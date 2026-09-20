from pathlib import Path
from datetime import date
from data_loader import DataStore
from product_matcher import match_product
from calendar_generator import generate_calendar

BASE=Path(__file__).resolve().parent
store=DataStore(BASE/"data")
examples=[
("Cloud Glaze","high shine; comfortable slip"),
("Peach Fizz Oil","peach tint; glossy cushion"),
("Berry Velvet Bullet","rich berry colour; creamy glide"),
("Cocoa Cloud Mask","rich texture; overnight-friendly routine"),
("Mint Reset Balm","conditioning feel; smooth glide"),
("Mystery Lip Potion","soft colour; lightweight feel")
]
for name,benefits in examples:
    product=match_product(name,benefits,store)
    calendar=generate_calendar(product,7,store,["Instagram","Pinterest"],date.today())
    print(f"\n{name} -> {len(calendar)} posts")
    print(calendar[["Platform","Customer Persona","Content Bucket","Image Title","Suggested Posting Time"]].head(3).to_string(index=False))
