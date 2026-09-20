from __future__ import annotations
from utils import clean_text

def choose_image_style(product, bucket, platform, store, index):
    images=store.images()
    category=str(product.get("Product Category","")).lower()
    suitable=images[images["Suitable Content Buckets"].str.contains(bucket,case=False,na=False)]
    if suitable.empty: suitable=images
    # Prefer product category matches, otherwise rotate.
    cat=suitable[suitable["Suitable Product Types"].str.contains(category.replace(" ","|"),case=False,na=False,regex=True)]
    if not cat.empty: suitable=cat
    return suitable.iloc[index % len(suitable)].to_dict()

def build_image_concept(product, bucket, style):
    name=clean_text(product.get("Product Name"))
    return {
        "Visual Concept": f"{style['Visual Style']} concept for {name}",
        "Composition": style["Composition"],
        "Product Placement": style["Product Placement"],
        "Background": style["Background"],
        "Lighting": style["Lighting"],
        "Props": style["Props"],
        "Model/Persona": style["Model/Persona"],
        "Mood": style["Colour Mood"],
        "Image Generation Prompt": (
            f"Create a {style['Visual Style'].lower()} beauty image featuring {name}. "
            f"Background: {style['Background']}. Lighting: {style['Lighting']}. "
            f"Props: {style['Props']}. Composition: {style['Composition']}. "
            f"Place the product {style['Product Placement']}. Mood: {style['Colour Mood']}."
        )
    }
