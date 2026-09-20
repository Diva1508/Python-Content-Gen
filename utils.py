from __future__ import annotations
from datetime import datetime
from pathlib import Path
import re

VALID_DURATIONS = {7, 14, 30}
STATUS_DRAFT = "Draft"
STATUS_SCHEDULED = "Scheduled"
STATUS_READY = "Ready to Publish"
STATUS_PUBLISHED = "Published"
STATUS_CANCELLED = "Cancelled"

def clean_text(value) -> str:
    return "" if value is None else str(value).strip()

def split_values(value) -> list[str]:
    text = clean_text(value)
    if not text:
        return []
    return [x.strip() for x in re.split(r";|,", text) if x.strip()]

def parse_time_window(window: str) -> tuple[int, int]:
    match = re.match(r"^\s*(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})\s*$", clean_text(window))
    if not match:
        raise ValueError(f"Invalid posting time window: {window}")
    h1,m1,h2,m2=map(int,match.groups())
    if h1>23 or h2>23 or m1>59 or m2>59:
        raise ValueError(f"Invalid posting time window: {window}")
    return h1*60+m1, h2*60+m2

def mid_time(window: str) -> str:
    a,b=parse_time_window(window)
    x=(a+b)//2
    return f"{x//60:02d}:{x%60:02d}"

def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+","-",clean_text(text).lower()).strip("-")

def validate_duration(value) -> int:
    try: n=int(value)
    except (TypeError,ValueError): raise ValueError("Campaign duration must be 7, 14 or 30 days.")
    if n not in VALID_DURATIONS: raise ValueError("Campaign duration must be 7, 14 or 30 days.")
    return n

def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")

def new_campaign_id() -> str:
    # Microsecond resolution keeps IDs unique even for back-to-back campaigns.
    return "CAMPAIGN_" + datetime.now().strftime("%Y%m%d%H%M%S%f")

def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
