from fastapi import APIRouter
from pydantic import BaseModel
from langchain_core.prompts import PromptTemplate
from transformers import pipeline
import re
import random

router = APIRouter()

class ProductInput(BaseModel):
    title: str
    brand: str
    categories: str
    material: str
    price: float

generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",
    max_new_tokens=80,
    temperature=0.7,
    top_p=0.9
)

prompt_template = PromptTemplate(
    input_variables=["title", "brand", "categories", "material", "price"],
    template=(
        "You are a product copywriter. Write a short, engaging, and realistic product description for a furniture item. "
        "Mention its material, brand, category, and price. Highlight its appeal for modern homes or offices.\n\n"
        "Product Details:\n"
        "Title: {title}\n"
        "Brand: {brand}\n"
        "Category: {categories}\n"
        "Material: {material}\n"
        "Price: ₹{price}\n\n"
        "Description:"
    ),
)

def generate_description_text(product: ProductInput) -> str:
    prompt = prompt_template.format(
        title=product.title,
        brand=product.brand,
        categories=product.categories,
        material=product.material,
        price=product.price,
    )

    raw = generator(prompt, num_return_sequences=1)[0]["generated_text"]
    text = raw.replace(prompt, "").strip()

    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\b(\w+)( \1\b)+", r"\1", text)
    text = re.sub(r"[^A-Za-z0-9\s,.₹]", "", text)
    parts = [s.strip().capitalize() for s in text.split(".") if 5 < len(s.strip()) < 140]

    final = ". ".join(parts[:2])
    if not final.endswith("."):
        final += "."

    if (
        not final
        or len(final.split()) < 6
        or len(set(final.lower().split())) < len(final.split()) * 0.6
    ):
        templates = [
            f"{product.title} by {product.brand} is crafted from premium {product.material}, offering both durability and elegance. Ideal for contemporary {product.categories.lower()} settings.",
            f"Experience comfort and style with the {product.brand} {product.title}, made from high-quality {product.material}. A perfect addition to any modern home or office.",
            f"Designed for lasting appeal, this {product.categories.lower()} piece by {product.brand} features sturdy {product.material} construction and a sleek finish.",
            f"The {product.title} blends timeless design with reliable craftsmanship. Built from {product.material}, it's a standout piece from {product.brand}.",
            f"Elevate your space with the {product.brand} {product.title} — a refined {product.categories.lower()} item made of durable {product.material}, priced at ₹{product.price}."
        ]
        final = random.choice(templates)

    return final
