from __future__ import annotations
from pathlib import Path
import pandas as pd
from utils import today, new_campaign_id

SCHEDULE_COLUMNS=["Post ID","Date","Time","Platform","Product","Customer Persona","Content Bucket","Content Type","Status"]
HISTORY_COLUMNS=["Campaign ID","Date Created","Product","Benefits","Campaign Duration","Number of Posts","Platforms","File Generated"]

def _load(path,columns):
    path=Path(path)
    if not path.exists(): return pd.DataFrame(columns=columns)
    return pd.read_csv(path,dtype=str,keep_default_na=False)

def save_scheduled(df,path):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(path,index=False,encoding="utf-8-sig")

def load_scheduled(path):
    return _load(path,SCHEDULE_COLUMNS)

def add_schedule(calendar_df,path):
    existing=load_scheduled(path)
    new=calendar_df[SCHEDULE_COLUMNS].copy()
    merged=pd.concat([existing,new],ignore_index=True).drop_duplicates(subset=["Post ID"],keep="last")
    save_scheduled(merged,path)
    return merged

def update_status(post_id,status,path):
    df=load_scheduled(path)
    if post_id not in df["Post ID"].values: raise ValueError(f"Post ID not found: {post_id}")
    df.loc[df["Post ID"]==post_id,"Status"]=status
    save_scheduled(df,path)
    return df

def cancel_post(post_id,path): return update_status(post_id,"Cancelled",path)
def mark_published(post_id,path): return update_status(post_id,"Published",path)

def upcoming(path,limit=20):
    df=load_scheduled(path)
    if df.empty: return df
    df["DateTime"]=pd.to_datetime(df["Date"]+" "+df["Time"],errors="coerce")
    out=df[df["Status"].isin(["Scheduled","Ready to Publish","Draft"])].sort_values("DateTime").head(limit).drop(columns=["DateTime"])
    return out

def mark_ready(path):
    df=load_scheduled(path)
    if df.empty: return df
    now=pd.Timestamp.now()
    dt=pd.to_datetime(df["Date"]+" "+df["Time"],errors="coerce")
    mask=(dt<=now)&(df["Status"]=="Scheduled")
    df.loc[mask,"Status"]="Ready to Publish"
    save_scheduled(df,path)
    return df

def add_history(product,benefits,duration,calendar_df,file_generated,path,campaign_id=None):
    df=_load(path,HISTORY_COLUMNS)
    row=pd.DataFrame([{
      "Campaign ID":campaign_id or new_campaign_id(),
      "Date Created":today(),"Product":product,"Benefits":benefits,
      "Campaign Duration":duration,"Number of Posts":len(calendar_df),
      "Platforms":", ".join(calendar_df["Platform"].drop_duplicates()),
      "File Generated":str(file_generated)
    }])
    pd.concat([df,row],ignore_index=True).to_csv(path,index=False,encoding="utf-8-sig")
