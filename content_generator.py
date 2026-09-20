from __future__ import annotations
import re
from utils import clean_text, split_values
from hashtag_generator import generate_hashtags
from image_generator import choose_image_style, build_image_concept
from posting_time import recommend_posting_time

def _first_match(df, col, value):
    if not value: return {}
    x=df[df[col].astype(str).str.lower()==str(value).lower()]
    return x.iloc[0].to_dict() if not x.empty else {}

def _template(store, platform,bucket,index):
    df=store.templates()
    x=df[(df["Platform"].str.lower()==platform.lower())&(df["Content Bucket"].str.lower()==bucket.lower())]
    if x.empty: x=df[df["Content Bucket"].str.lower()==bucket.lower()]
    if x.empty: x=df[df["Platform"].str.lower()==platform.lower()]
    if x.empty: x=df
    return x.iloc[index%len(x)].to_dict()

def _hook(store,bucket,index):
    hooks=store.hooks()
    category_map={"Education":"Education","Product Spotlight":"Product","Lip Care Tips":"Problem/Solution",
                  "Lifestyle":"Lifestyle","Entertainment":"Humour","Engagement":"Engagement",
                  "Social Proof":"Emotional","Flavour/Sensory":"Curiosity","Ingredient Spotlight":"Education",
                  "Brand Story":"Storytelling","Community":"Engagement","Promotion":"Product"}
    x=hooks[hooks["Category"]==category_map.get(bucket,"Product")]
    if x.empty: x=hooks
    return x.iloc[index%len(x)].to_dict()

def _cta(store,bucket,index):
    df=store.ctas()
    cat_map={"Product Spotlight":"Product discovery","Promotion":"Promotion","Engagement":"Comment",
             "Community":"Comment","Education":"Save","Lip Care Tips":"Save","Ingredient Spotlight":"Save",
             "Lifestyle":"Save","Entertainment":"Share","Flavour/Sensory":"Comment","Brand Story":"Follow",
             "Social Proof":"Product discovery"}
    x=df[df["Category"]==cat_map.get(bucket,"Engagement")]
    if x.empty: x=df
    return x.iloc[index%len(x)]["CTA"]

def _platform_intro(platform,bucket):
    intros={
      "Instagram":f"{bucket.lower()} made simple.",
      "LinkedIn":f"A useful thought about {bucket.lower()} in beauty.",
      "Facebook":f"Here is a simple beauty idea for your routine.",
      "Pinterest":f"A lip idea worth saving.",
      "YouTube Shorts":"Watch the lip detail up close."
    }
    return intros.get(platform,"A simple lip idea.")

def generate_post(plan_row, product, persona, store, index, campaign_id=""):
    platform=plan_row["Platform"]; bucket=plan_row["Content Bucket"]
    p=store.platforms()
    pr=p[p["Platform"]==platform].iloc[0].to_dict()
    template=_template(store,platform,bucket,index)
    hook=_hook(store,bucket,index)
    cta=_cta(store,bucket,index)
    brand=store.brand()
    flavour=clean_text(product.get("Flavour"))
    ingredients=clean_text(product.get("Key Ingredients"))
    benefits=clean_text(product.get("Entered Benefits")) or clean_text(product.get("Key Benefits"))
    finish=clean_text(product.get("Finish"))
    texture=clean_text(product.get("Texture"))
    shade=clean_text(product.get("Shade"))
    main=(
      f"{_platform_intro(platform,bucket)}\n\n"
      f"{product['Product Name']} brings {benefits.lower() if benefits else 'an easy lip moment'}"
      f"{f' with a {texture.lower()} texture' if texture else ''}"
      f"{f' and a {finish.lower()} finish' if finish else ''}."
    )
    if flavour: main += f" The {flavour.lower()} flavour adds a sensory detail to the routine."
    if shade: main += f" The {shade.lower()} shade keeps the colour story easy to wear."
    if ingredients and bucket=="Ingredient Spotlight":
        main += f" Formula story: {ingredients}."
    main += f"\n\nDesigned for {persona['Persona Name'].lower()}s, this fits a routine built around {persona['Main Needs'].lower()}."
    # Platform-specific shaping
    if platform=="LinkedIn":
        main=(f"{hook['Hook Structure']}\n\n"
              f"For {brand['Brand Name']}, this is where {bucket.lower()} becomes useful content. "
              f"{main}\n\nThe point is simple: explain the product clearly, then give people a reason to remember it.")
    elif platform=="YouTube Shorts":
        main=f"Scene 1: Show {product['Product Name']}.\nScene 2: Show the texture and shade.\nScene 3: Show the product in a {persona['Persona Name'].lower()} routine.\nOn-screen text: {hook['Hook Structure']}"
    elif platform=="Pinterest":
        main=f"{hook['Hook Structure']}\n\n{main}\n\nSave this idea for later."
    hashtags=generate_hashtags(product,persona,bucket,platform,store,index)
    style=choose_image_style(product,bucket,platform,store,index)
    visual=build_image_concept(product,bucket,style)
    image_title=f"{product['Product Name']} | {bucket}"
    alt=f"{product['Product Name']}, {product.get('Product Category','lip product').lower()}, shown in a {style['Visual Style'].lower()} beauty setup"
    return {
      "Post ID":f"{campaign_id + '_' if campaign_id else ''}POST_{index+1:03d}",
      "Date":plan_row["Date"],"Day":__import__("datetime").date.fromisoformat(plan_row["Date"]).strftime("%A"),
      "Time":recommend_posting_time(platform,__import__("datetime").date.fromisoformat(plan_row["Date"]).strftime("%A"),
                                   persona["Persona ID"],bucket,template.get("Content Bucket",""),store,index),
      "Platform":platform,"Product":product["Product Name"],"Customer Persona":persona["Persona Name"],
      "Persona ID":persona["Persona ID"],"Content Bucket":bucket,
      "Content Type":template.get("Visual Structure","Static image post"),
      "Hook":hook["Hook Structure"],"Post Content":main,"CTA":cta,"Hashtags/meta tags":hashtags,
      "Image Concept":visual["Visual Concept"],"Composition":visual["Composition"],
      "Product Placement":visual["Product Placement"],"Background":visual["Background"],
      "Lighting":visual["Lighting"],"Props":visual["Props"],"Model/Persona":visual["Model/Persona"],
      "Mood":visual["Mood"],"Image Generation Prompt":visual["Image Generation Prompt"],
      "Image Title":image_title,"Alt Text":alt,"Suggested Posting Time":plan_row["Time Window"],
      "Status":"Draft"
    }
