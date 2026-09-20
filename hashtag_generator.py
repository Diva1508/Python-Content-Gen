from __future__ import annotations
from collections import defaultdict
from utils import split_values

def generate_hashtags(product, persona, bucket, platform, store, index):
    tags=store.hashtags()
    category=str(product.get("Product Category","")).lower()
    chosen=[]
    # Match product category, bucket, and persona vocabulary to library categories/keywords.
    wanted=[]
    if "gloss" in category: wanted+=["Lip Gloss","Lip Makeup","Product discovery"]
    elif "oil" in category: wanted+=["Lip Oil","Lip Care","Product discovery"]
    elif "lipstick" in category: wanted+=["Lipstick","Lip Makeup","Product discovery"]
    elif "mask" in category: wanted+=["Lip Mask","Lip Care","Self-care"]
    elif "balm" in category: wanted+=["Lip Care","Lip Makeup","Product discovery"]
    else: wanted+=["Lip Care","Beauty","Product discovery"]
    if bucket in ["Ingredient Spotlight"]: wanted+=["Ingredients"]
    if bucket in ["Lifestyle"]: wanted+=["Lifestyle","Self-care"]
    if bucket in ["Community","Engagement"]: wanted+=["Audience"]
    for cat in wanted:
        subset=tags[tags["Category"]==cat]
        for _,r in subset.iterrows():
            if r["Tag/Keyword"] not in chosen: chosen.append(r["Tag/Keyword"])
    # Rotate the set so posts do not receive identical tags.
    if not chosen: return ""
    offset=index % len(chosen)
    rotated=chosen[offset:]+chosen[:offset]
    return " ".join(rotated[:6])
