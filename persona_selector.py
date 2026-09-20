from __future__ import annotations
from utils import split_values, clean_text

def select_persona(product, store, used_persona_ids=None):
    used=set(used_persona_ids or [])
    text=" ".join(str(product.get(k,"")) for k in [
        "Product Category","Product Description","Key Benefits","Hero Benefit",
        "Secondary Benefits","Ingredient Benefits","Flavour","Texture","Finish",
        "Product Personality","Main Marketing Angle","Suggested Content Buckets"
    ]).lower()
    category=str(product.get("Product Category","")).lower()
    candidates=[]
    for _,p in store.personas().iterrows():
        score=0
        prefs=" ".join(str(p.get(k,"")) for k in ["Preferred Products","Preferred Flavours","Preferred Finishes","Ingredient Interests","Preferred Content Buckets"]).lower()
        if category and category in prefs: score+=5
        for token in set(text.replace(";"," ").split()):
            if len(token)>3 and token in prefs: score+=1
        if p["Persona ID"] in used: score-=3
        candidates.append((score,p))
    candidates.sort(key=lambda x:(x[0], -len(used & {x[1]["Persona ID"]})), reverse=True)
    return candidates[0][1].to_dict()
