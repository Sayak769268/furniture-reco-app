from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import os, json, re, ast
from dotenv import load_dotenv
from pathlib import Path

from app.generate_description import ProductInput, generate_description_text

router = APIRouter()

# Load .env
env_path = Path(__file__).resolve().parents[0] / ".env"
load_dotenv(dotenv_path=env_path, override=True)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")

# Embeddings
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def get_index():
    client = Pinecone(api_key=PINECONE_API_KEY)
    return client.Index(PINECONE_INDEX)

# Lightweight LLM for intent parsing
llm_pipe = pipeline(
    "text-generation",
    model="distilgpt2",
    max_new_tokens=80,
    temperature=0.5,
    top_p=0.9,
    do_sample=True
)
llm = HuggingFacePipeline(pipeline=llm_pipe)

intent_prompt = PromptTemplate(
    input_variables=["message", "history"],
    template=(
        "You are an assistant helping select furniture.\n"
        "Extract a clean search query and constraints from the user's message and prior context.\n"
        "Return JSON with keys: query, room, style, material, color, min_price, max_price.\n"
        "If unknown, use null.\n\n"
        "History:\n{history}\n\n"
        "Message:\n{message}\n\n"
        "JSON:"
    ),
)

class ChatTurn(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    user_message: str
    history: Optional[List[ChatTurn]] = []

# --- helper to clean images ---
def clean_images(images):
    if not images:
        return []
    if isinstance(images, list):
        return [i.strip() for i in images if isinstance(i, str) and i.strip().startswith("http")]
    if isinstance(images, str):
        try:
            parsed = ast.literal_eval(images)
            if isinstance(parsed, list):
                return [i.strip() for i in parsed if isinstance(i, str) and i.strip().startswith("http")]
        except Exception:
            pass
        return [i.strip(" '") for i in images.split(",") if i.strip().startswith("http")]
    return []

# --- helper to clean/parse prices ---
def parse_price(val):
    if not val:
        return None
    try:
        return float(str(val).replace("$", "").replace(",", "").strip())
    except Exception:
        return None

@router.post("/recommend/chat")
def recommend_chat(req: ChatRequest) -> Dict[str, Any]:
    try:
        # 1) Parse intent
        history_text = "\n".join([f"{t.role}: {t.content}" for t in (req.history or [])])
        intent_input = intent_prompt.format(message=req.user_message, history=history_text)

        intent = {
            "query": req.user_message,
            "room": None,
            "style": None,
            "material": None,
            "color": None,
            "min_price": None,
            "max_price": None,
        }

        try:
            raw = llm_pipe(intent_input)
            text = raw[0]["generated_text"]
            json_like = re.search(r"\{.*\}", text, re.S)
            if json_like:
                intent = {**intent, **json.loads(json_like.group(0))}
        except Exception:
            pass  # fallback to defaults

        # 2) Build search text
        parts = [intent.get("query") or req.user_message]
        for k in ["room", "style", "material", "color"]:
            v = intent.get(k)
            if v: parts.append(str(v))
        search_text = " ".join(parts)

        # 3) Query Pinecone
        qvec = embedder.encode(search_text).tolist()
        index = get_index()
        results = index.query(vector=qvec, top_k=8, include_metadata=True)

        # 4) Filter + format
        recs: List[Dict[str, Any]] = []
        for m in results.get("matches", []):
            md = m.get("metadata", {}) or {}

            # price parsing + filter
            price_val = parse_price(md.get("price"))
            lo, hi = intent.get("min_price"), intent.get("max_price")
            if lo is not None and price_val and price_val < float(lo): 
                continue
            if hi is not None and price_val and price_val > float(hi): 
                continue

            title = md.get("title") or "Furniture item"
            brand = md.get("brand") or "Unknown brand"
            categories = md.get("categories")
            if isinstance(categories, list):
                categories = ", ".join(categories)
            elif isinstance(categories, str) and categories.startswith("["):
                try:
                    parsed_c = ast.literal_eval(categories)
                    categories = ", ".join(parsed_c) if isinstance(parsed_c, list) else str(parsed_c)
                except Exception:
                    pass
            categories = categories or "home"
            material = md.get("material") or "premium materials"

            # description
            pinput = ProductInput(
                title=title, brand=brand, categories=categories, material=material, price=price_val or 0
            )
            gen_desc = generate_description_text(pinput)

            recs.append({
                "id": m.get("id"),
                "score": m.get("score"),
                "title": title,
                "brand": brand,
                "price": price_val,
                "categories": categories,
                "material": material,
                "color": md.get("color"),
                "images": clean_images(md.get("images")),
                "description": md.get("description"),
                "generated_description": gen_desc
            })
            if len(recs) >= 6:
                break

        # 5) Return
        return {
            "message": "Here are some options I found for you!",
            "intent": intent,
            "search_text": search_text,
            "recommendations": recs
        }

    except Exception as e:
        import traceback; traceback.print_exc()
        return {"error": str(e)}
