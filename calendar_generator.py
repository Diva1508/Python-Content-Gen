from __future__ import annotations
import pandas as pd
from datetime import date,timedelta
from content_generator import generate_post
from persona_selector import select_persona
from utils import new_campaign_id

def generate_calendar(product,duration,store,platforms=None,start_date=None,campaign_id=None):
    from content_planner import plan_campaign
    campaign_id=campaign_id or new_campaign_id()
    plan=plan_campaign(product,duration,store,platforms,start_date)
    posts=[]; used=[]
    personas_by_id={p["Persona ID"]:p for _,p in store.personas().iterrows()}
    for i,row in enumerate(plan):
        pid=row["Persona ID"]
        persona=personas_by_id.get(pid)
        if persona is None:
            persona=select_persona(product,store,used)
        used.append(persona["Persona ID"])
        posts.append(generate_post(row,product,persona,store,i,campaign_id))
    df=pd.DataFrame(posts)
    return df.sort_values(["Date","Time","Platform"]).reset_index(drop=True)
