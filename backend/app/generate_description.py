from fastapi import APIRouter
from pydantic import BaseModel
from langchain_core.prompts import PromptTemplate
from transformers import pipeline
import re
import random

router = APIRouter()

# Input schema
class ProductInput(BaseModel):
    title: str
    brand: str
    categories: str
    material: str
    price: float

# Use small GPT-2 model
generator = pipeline(
    "text-generation",
    model="distilgpt2",
    max_new_tokens=60,
    temperature=0.6,
    top_p=0.85,
    do_sample=True
)

# Prompt template — shorter and stricter
prompt_template = PromptTemplate(
    input_variables=["title", "brand", "categories", "material", "price"],
    template=(
        "Write two short, simple, and realistic sentences describing a furniture product. "
        "Avoid repeating words. Keep it factual, clear, and natural.\n\n"
        "Title: {title}\n"
        "Brand: {brand}\n"
        "Category: {categories}\n"
        "Material: {material}\n"
        "Price: ₹{price}\n\n"
        "Description:"
    ),
)

@router.post("/generate/description")
def generate_description(product: ProductInput):
    try:
        prompt = prompt_template.format(
            title=product.title,
            brand=product.brand,
            categories=product.categories,
            material=product.material,
            price=product.price,
        )

        result = generator(prompt, num_return_sequences=1)[0]["generated_text"]
        text = result.replace(prompt, "").strip()

        # Clean up output
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\b(\w+)( \1\b)+", r"\1", text)  # remove repeated words
        text = re.sub(r"[^A-Za-z0-9\s,.]", "", text)   # remove symbols
        text = text.split(".")
        sentences = [s.strip().capitalize() for s in text if 5 < len(s.strip()) < 120]

        final = ". ".join(sentences[:2])
        if not final.endswith("."):
            final += "."

        # Fallback if nonsense or repetition remains
        if (
            not final
            or len(final.split()) < 6
            or len(set(final.lower().split())) < len(final.split()) * 0.6
        ):
            templates = [
                f"{product.title} by {product.brand} is crafted from {product.material} for durability and style. Perfect for modern {product.categories.lower()} spaces.",
                f"The {product.brand} {product.title} combines elegant {product.material} with reliable quality. A great fit for any home or office.",
                f"Designed by {product.brand}, this {product.categories.lower()} piece is made from {product.material} for a timeless and sturdy look."
            ]
            final = random.choice(templates)

        return {"generated_description": final}

    except Exception as e:
        import traceback; traceback.print_exc()
        return {"error": str(e)}

def generate_description_text(product: ProductInput) -> str:
    # Build prompt
    prompt = prompt_template.format(
        title=product.title,
        brand=product.brand,
        categories=product.categories,
        material=product.material,
        price=product.price,
    )

    # Generate text
    raw = generator(prompt, num_return_sequences=1)[0]["generated_text"]
    text = raw.replace(prompt, "").strip()

    # Clean & trim
    import re, random
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\b(\w+)( \1\b)+", r"\1", text)  # remove immediate repeats
    text = re.sub(r"[^A-Za-z0-9\s,.]", "", text)
    parts = [s.strip().capitalize() for s in text.split(".") if 5 < len(s.strip()) < 120]

    final = ". ".join(parts[:2])
    if not final.endswith("."):
        final += "."

    # Fallback if weak or too repetitive
    if (
        not final
        or len(final.split()) < 6
        or len(set(final.lower().split())) < len(final.split()) * 0.6
    ):
        templates = [
            f"{product.title} by {product.brand} is crafted from {product.material} for durability and style. Perfect for modern {product.categories.lower()} spaces.",
            f"The {product.brand} {product.title} combines elegant {product.material} with reliable quality. A great fit for any home or office.",
            f"Designed by {product.brand}, this {product.categories.lower()} piece is made from {product.material} for a timeless and sturdy look."
        ]
        final = random.choice(templates)

    return final
