from fastapi import APIRouter, Query
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import os
from dotenv import load_dotenv
from pathlib import Path
import ast  # for safely parsing stringified lists

# Import the reusable generator helper and input model
from app.generate_description import ProductInput, generate_description_text

router = APIRouter()

# Load .env from app/.env (since your .env is inside app/)
env_path = Path(__file__).resolve().parents[0] / ".env"
load_dotenv(dotenv_path=env_path, override=True)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")

# Load embedder once (lighter model for deployment)
embedder = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L3-v2")


def get_index():
    client = Pinecone(api_key=PINECONE_API_KEY)
    return client.Index(PINECONE_INDEX)

@router.get("/search")
def search_products(
    query: str = Query(..., min_length=3),
    top_k: int = 5
) -> Dict[str, Any]:
    try:
        # 1) Embed query
        query_vec = embedder.encode(query).tolist()

        # 2) Query Pinecone
        index = get_index()
        results = index.query(
            vector=query_vec,
            top_k=top_k,
            include_metadata=True
        )

        # 3) Format results and enrich with generated descriptions
        matches: List[Dict[str, Any]] = []
        for m in results["matches"]:
            md = m.get("metadata", {}) or {}

            # Defensive defaults
            title = md.get("title") or "Furniture item"
            brand = md.get("brand") or "Unknown brand"

            # --- Clean categories ---
            raw_categories = md.get("categories") or "home"
            if isinstance(raw_categories, str):
                try:
                    parsed = ast.literal_eval(raw_categories)
                    if isinstance(parsed, list):
                        categories = ", ".join(parsed)
                    else:
                        categories = str(parsed)
                except Exception:
                    categories = raw_categories
            elif isinstance(raw_categories, list):
                categories = ", ".join(raw_categories)
            else:
                categories = str(raw_categories)

            material = md.get("material") or "premium materials"

            price_val = md.get("price")
            try:
                price = float(price_val) if price_val is not None else 0.0
            except Exception:
                price = 0.0

            # Build ProductInput for description generation
            product_input = ProductInput(
                title=title,
                brand=brand,
                categories=categories,
                material=material,
                price=price
            )

            generated_desc = generate_description_text(product_input)

            # Append final result
            matches.append({
                "id": m.get("id"),
                "score": m.get("score"),
                "title": title,
                "brand": brand,
                "price": price,
                "categories": categories,
                "material": material,
                "color": md.get("color"),
                "images": md.get("images"),
                "description": md.get("description"),  # original description from metadata (if any)
                "generated_description": generated_desc  # new AI-generated description
            })

        return {"query": query, "count": len(matches), "results": matches}

    except Exception as e:
        import traceback; traceback.print_exc()
        return {"error": str(e)}
