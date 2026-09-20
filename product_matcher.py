from __future__ import annotations
import re
from utils import split_values, clean_text

def _tokens(text):
    return set(re.findall(r"[a-z0-9]+", clean_text(text).lower()))

def match_product(name, benefits, store):
    products=store.products()
    target=clean_text(name).lower()
    exact=products[products["Product Name"].str.lower()==target]
    if not exact.empty:
        row=exact.iloc[0].to_dict()
        row["Entered Benefits"]=clean_text(benefits)
        row["Is Temporary Product"]="No"
        return row

    # Unknown products get a temporary profile. We only borrow attributes
    # when their text provides a reasonable semantic overlap.
    benefit_tokens=_tokens(benefits)
    candidates=[]
    for _,row in products.iterrows():
        text=" ".join(str(row.get(c,"")) for c in ["Product Name","Product Category","Product Description","Key Benefits","Main Marketing Angle"])
        overlap=len(benefit_tokens & _tokens(text))
        candidates.append((overlap,row))
    candidates.sort(key=lambda x:x[0],reverse=True)
    best=candidates[0][1] if candidates and candidates[0][0]>0 else None

    temp={
        "Product ID":"TEMP_001","Product Name":clean_text(name),
        "Product Category":"Custom Product","Product Subcategory":"User-entered",
        "Product Description":f"{clean_text(name)} designed around the user's stated benefits.",
        "Key Benefits":clean_text(benefits),"Hero Benefit":clean_text(benefits),
        "Secondary Benefits":"","Key Ingredients":"","Ingredient Benefits":"",
        "Flavour":"","Scent":"","Texture":"","Finish":"","Shade":"","Shade Family":"",
        "Shade Description":"","Ideal Use":"As directed by the product concept",
        "Recommended Time of Day":"Anytime","Suitable Customer Persona":"",
        "Price Tier":"","Product Personality":"user-defined","Main Marketing Angle":clean_text(benefits),
        "Secondary Marketing Angles":"","Suggested CTA":"Explore the product",
        "Suggested Content Buckets":"","Suitable Platforms":"",
        "Image Concept":"","Visual Mood":"","Entered Benefits":clean_text(benefits),
        "Is Temporary Product":"Yes"
    }
    if best is not None and candidates[0][0] >= 2:
        # Borrow only clearly related descriptive fields, not an unrelated identity.
        for col in ["Texture","Finish","Ideal Use","Recommended Time of Day","Product Personality","Visual Mood"]:
            temp[col]=best.get(col,"")
    return temp
