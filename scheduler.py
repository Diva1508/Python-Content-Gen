from __future__ import annotations
from storage import load_scheduled, add_schedule, update_status, cancel_post, mark_published, upcoming, mark_ready

def schedule_calendar(calendar_df,path):
    df=add_schedule(calendar_df,path)
    # New generated posts begin as Draft. User explicitly schedules selected posts later.
    return df

def schedule_post(post_id,date,time,path):
    df=load_scheduled(path)
    if post_id not in df["Post ID"].values: raise ValueError(f"Post ID not found: {post_id}")
    df.loc[df["Post ID"]==post_id,["Date","Time","Status"]]=[date,time,"Scheduled"]
    df.to_csv(path,index=False,encoding="utf-8-sig")
    return df

def cancel_scheduled_post(post_id,path): return cancel_post(post_id,path)
def publish_post(post_id,path): return mark_published(post_id,path)
def ready_posts(path): return mark_ready(path)
def view_upcoming(path,limit=20): return upcoming(path,limit)
