from __future__ import annotations
import math
from collections import Counter
from datetime import date,timedelta
from utils import split_values

def _largest_remainder(weights, total):
    raw={k:weights[k]*total for k in weights}
    counts={k:int(math.floor(v)) for k,v in raw.items()}
    remaining=total-sum(counts.values())
    order=sorted(weights,key=lambda k:raw[k]-counts[k],reverse=True)
    for k in order[:remaining]: counts[k]+=1
    return counts

def choose_platforms(store, requested=None):
    available=store.platforms()["Platform"].tolist()
    if requested:
        chosen=[p for p in requested if p in available]
        if chosen: return chosen
    return available

def plan_campaign(product, duration, store, platforms=None, start_date=None):
    platforms=choose_platforms(store,platforms)
    start=start_date or date.today()
    buckets=store.buckets()
    weights={r["Bucket Name"]:float(r["Recommended Percentage of Total Content"])/100 for _,r in buckets.iterrows()}
    counts=_largest_remainder(weights,duration)
    # If rounding yields zero for many buckets, use only positive allocations.
    sequence=[]
    used_last=None
    for bucket,count in counts.items():
        for _ in range(count):
            sequence.append(bucket)
    # Interleave to avoid consecutive identical buckets.
    ordered=[]
    while sequence:
        options=[x for x in sequence if x!=used_last] or sequence
        chosen=options[0]
        sequence.remove(chosen)
        ordered.append(chosen); used_last=chosen

    # campaign_structure is the source of day-level intent where it exists.
    cs=store.campaign_structure()
    cs=cs[cs["Campaign Duration"].astype(str)==str(duration)]
    rows=[]
    used_personas=[]
    times=store.times()
    for i,bucket in enumerate(ordered):
        day_index=i
        day=(start+timedelta(days=day_index)).isoformat()
        platform=platforms[i%len(platforms)]
        matching=times[(times["Platform"]==platform)&(times["Content Bucket"]==bucket)]
        if matching.empty:
            matching=times[times["Platform"]==platform]
        if not matching.empty:
            r=matching.iloc[i%len(matching)]
            persona_id=r["Audience/Persona"]
            # Prefer varied personas when possible.
            pids=[x for x in matching["Audience/Persona"].unique() if x not in used_personas]
            if pids: persona_id=pids[0]
            window=r["Time Window"]
        else:
            persona_id=""
            window="18:00-20:00"
        if persona_id: used_personas.append(persona_id)
        rows.append({"Day Number":i+1,"Date":day,"Platform":platform,"Content Bucket":bucket,
                     "Persona ID":persona_id,"Time Window":window})
    return rows
