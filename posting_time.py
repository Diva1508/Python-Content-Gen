from __future__ import annotations
from utils import mid_time

def recommend_posting_time(platform, day, persona_id, bucket, content_type, store, index=0):
    times=store.times()
    matches=times[(times["Platform"]==platform)&(times["Day"]==day)&
                  (times["Audience/Persona"]==persona_id)&(times["Content Bucket"]==bucket)]
    if matches.empty:
        matches=times[(times["Platform"]==platform)&(times["Day"]==day)&
                      (times["Content Bucket"]==bucket)]
    if matches.empty:
        matches=times[(times["Platform"]==platform)&(times["Day"]==day)]
    if matches.empty:
        matches=times[times["Platform"]==platform]
    if matches.empty:
        return "18:00"
    row=matches.iloc[index % len(matches)]
    return mid_time(row["Time Window"])
