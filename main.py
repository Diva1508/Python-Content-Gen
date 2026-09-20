from __future__ import annotations
from pathlib import Path
from datetime import date
import pandas as pd

from data_loader import DataStore, DataLoadError
from product_matcher import match_product
from calendar_generator import generate_calendar
from excel_exporter import export_calendar
from storage import add_history, load_scheduled
from scheduler import schedule_post, cancel_scheduled_post, publish_post, ready_posts, view_upcoming
from utils import new_campaign_id

BASE_DIR=Path(__file__).resolve().parent
DATA_DIR=BASE_DIR/"data"
OUTPUT_DIR=BASE_DIR/"output"
SCHEDULE_FILE=OUTPUT_DIR/"scheduled_posts.csv"
HISTORY_FILE=OUTPUT_DIR/"campaign_history.csv"

def choose_platforms(store):
    available=store.platforms()["Platform"].tolist()
    answer=input(f"Platforms to include, comma-separated, or press Enter for all ({', '.join(available)}): ").strip()
    if not answer: return available
    selected=[x.strip() for x in answer.split(",") if x.strip() in available]
    if not selected:
        print("No valid platforms selected. Using all available platforms.")
        return available
    return selected

def generate_flow(store):
    name=input("Product name: ").strip()
    if not name: print("Error: Product name cannot be empty."); return
    benefits=input("Product benefits: ").strip()
    if not benefits: print("Error: Product benefits cannot be empty."); return
    try: duration=int(input("Campaign duration [7/14/30], default 7: ").strip() or "7")
    except ValueError: print("Error: Campaign duration must be 7, 14 or 30."); return
    if duration not in [7,14,30]: print("Error: Campaign duration must be 7, 14 or 30."); return
    platforms=choose_platforms(store)
    product=match_product(name,benefits,store)
    if product["Is Temporary Product"]=="Yes":
        print("Product not found. Using a temporary profile based on your name and benefits.")
    else:
        print(f"Matched existing product: {product['Product Name']}")
    campaign_id=new_campaign_id()
    calendar=generate_calendar(product,duration,store,platforms,date.today(),campaign_id)
    xlsx=OUTPUT_DIR/"Social_Media_Calendar.xlsx"
    export_calendar(calendar,xlsx,product,duration)
    from storage import add_schedule
    add_schedule(calendar,SCHEDULE_FILE)
    add_history(product["Product Name"],benefits,duration,calendar,xlsx,HISTORY_FILE,campaign_id)
    print(f"\nCampaign generated: {len(calendar)} posts")
    print(f"Excel calendar: {xlsx}")
    print("\nFirst 5 posts:")
    print(calendar[["Date","Time","Platform","Product","Customer Persona","Content Bucket","Status"]].head().to_string(index=False))

def scheduler_menu(store):
    while True:
        print("\nScheduler")
        print("1. View scheduled/upcoming posts")
        print("2. Schedule a post")
        print("3. Cancel a scheduled post")
        print("4. Mark a post as published")
        print("5. Mark due scheduled posts as READY TO PUBLISH")
        print("0. Back")
        choice=input("Choose: ").strip()
        try:
            if choice=="1": print(view_upcoming(SCHEDULE_FILE).to_string(index=False) or "No posts.")
            elif choice=="2":
                pid=input("Post ID: ").strip(); d=input("Date YYYY-MM-DD: ").strip(); t=input("Time HH:MM: ").strip()
                schedule_post(pid,d,t,SCHEDULE_FILE); print("Post scheduled.")
            elif choice=="3":
                pid=input("Post ID: ").strip(); cancel_scheduled_post(pid,SCHEDULE_FILE); print("Post cancelled.")
            elif choice=="4":
                pid=input("Post ID: ").strip(); publish_post(pid,SCHEDULE_FILE); print("Post marked Published.")
            elif choice=="5":
                ready_posts(SCHEDULE_FILE); print("Due posts updated.")
            elif choice=="0": return
            else: print("Choose a valid option.")
        except Exception as exc: print(f"Error: {exc}")

def main():
    try: store=DataStore(DATA_DIR)
    except DataLoadError as exc:
        print(f"Data loading error: {exc}"); return
    print("\nBeauty & Skincare Social Media Content Generator")
    print("Fully local command-line backend")
    while True:
        print("\n1. Generate campaign")
        print("2. Local scheduler")
        print("3. Exit")
        choice=input("Choose: ").strip()
        if choice=="1": generate_flow(store)
        elif choice=="2": scheduler_menu(store)
        elif choice=="3": print("Goodbye."); break
        else: print("Choose 1, 2 or 3.")

if __name__=="__main__":
    main()
