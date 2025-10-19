from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import your route modules
from app import (
    data_preview,
    embed_and_index,
    search,
    generate_description,
    analytics,
    recommend,
)

app = FastAPI(title="Furniture Recommendation API")

# --- CORS setup ---
# Allow local frontend (Vite dev server) and later your Netlify domain
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "*"  # you can restrict this later to your deployed frontend domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
app.include_router(data_preview.router, prefix="/data", tags=["data"])
app.include_router(embed_and_index.router, prefix="/embed", tags=["embed"])
app.include_router(search.router, prefix="", tags=["search"])
app.include_router(generate_description.router, prefix="", tags=["genai"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
app.include_router(recommend.router, prefix="", tags=["recommend"])

# --- Root route ---
@app.get("/")
def root():
    return {"message": "Furniture Recommendation API is running"}
