from fastapi import APIRouter
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

router = APIRouter()

# Load .env
env_path = Path(__file__).resolve().parents[0] / ".env"
load_dotenv(dotenv_path=env_path, override=True)

api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX")

print("🔑 API Key:", api_key[:8])
print("📦 Index Name:", index_name)

@router.get("/index")
def index_products():
    try:
        # Load product data
        df = pd.read_csv("app/data/products.csv").fillna("")
        df["search_text"] = df.apply(
            lambda r: f"{r['title']} {r['brand']} {r['description']} {r['categories']} {r['material']} {r['color']}",
            axis=1
        )

        # Generate embeddings locally
        # Generate embeddings locally (lighter model for deployment)
        embedder = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L3-v2")
        vectors = embedder.encode(df["search_text"].tolist(), show_progress_bar=True)

        # Initialize Pinecone client
        client = Pinecone(api_key=api_key)

        # Create index if needed
        if index_name not in [i.name for i in client.list_indexes()]:
            client.create_index(name=index_name, dimension=384)

        index = client.Index(index_name)

        # Prepare items for upsert
        items = []
        for i, row in df.iterrows():
            meta = {
                "title": row["title"],
                "brand": row["brand"],
                "description": row["description"],
                "categories": row["categories"],
                "material": row["material"],
                "color": row["color"],
                "price": row["price"],
                "images": row["images"]
            }
            items.append((str(row["uniq_id"]), vectors[i].tolist(), meta))

        # Upload to Pinecone
        index.upsert(items)
        print(f" Indexed {len(items)} items to Pinecone")
        return {"indexed": len(items)}

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}
