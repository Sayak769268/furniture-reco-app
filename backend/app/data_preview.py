from fastapi import APIRouter
import pandas as pd

router = APIRouter()  

@router.get("/preview")
def preview_data():
    try:
        df = pd.read_csv("app/data/products.csv")
        df = df.fillna("")
        sample = df.head(5).to_dict(orient="records")
        return {"sample": sample}
    except Exception as e:
        print("Error loading CSV:", e)
        return {"error": str(e)}
