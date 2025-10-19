from fastapi import APIRouter
import pandas as pd
from pathlib import Path

router = APIRouter()

@router.get("/summary")
def analytics_summary():
    path = Path(__file__).resolve().parent / "data" / "Products.csv"
    df = pd.read_csv(path)

    return {
    "summary": {
        "total_products": int(len(df)),
        "with_price": int(df["price"].notnull().sum())
    }
}
