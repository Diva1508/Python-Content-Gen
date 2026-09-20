# Beauty & Skincare Social Media Content Generator

A fully local, command-line Python backend for generating beauty and lip-care social media campaigns from pre-fed CSV data.

## Features

- User enters only product name and product benefits.
- Optional 7, 14 or 30 day campaign duration.
- Optional platform selection.
- Loads brand, product, persona, bucket, platform, timing, template, hook, CTA, hashtag and image-rule data from CSV.
- Matches known products and creates a temporary profile for unknown products.
- Selects personas automatically.
- Maintains content bucket percentages with largest-remainder rounding.
- Avoids consecutive identical content buckets where possible.
- Generates platform-specific post structures.
- Generates image concepts, image-generation prompts, titles and alt text.
- Creates a chronological Excel social media calendar.
- Provides a local scheduler with Draft, Scheduled, Ready to Publish, Published and Cancelled states.
- Stores campaign history locally.

## Folder structure

```text
marketing_content_generator/
├── main.py
├── data_loader.py
├── product_matcher.py
├── persona_selector.py
├── content_planner.py
├── content_generator.py
├── hashtag_generator.py
├── image_generator.py
├── posting_time.py
├── calendar_generator.py
├── scheduler.py
├── excel_exporter.py
├── storage.py
├── utils.py
├── demo.py
├── requirements.txt
├── README.md
├── data/
└── output/
```

## Installation

1. Install Python 3.10 or newer.
2. Open a terminal inside the project folder.
3. Run:

```bash
python -m pip install -r requirements.txt
```

## How to run

```bash
python main.py
```

Choose `1` to generate a campaign.

Enter:
- Product name
- Product benefits
- Campaign duration: 7, 14 or 30
- Optional platforms

The program creates `output/Social_Media_Calendar.xlsx`.

## How product matching works

The program first checks `product_catalogue.csv` for an exact product-name match. Known products use their stored data. Unknown products get a temporary profile using the user's product name and benefits. The matcher only borrows descriptive fields when benefit text has a reasonable overlap with the catalogue.

User-entered benefits take priority over stored generic benefits.

## How campaign planning works

The planner reads the recommended percentages in `content_buckets.csv`, converts them into whole-post allocations using largest-remainder rounding, then interleaves buckets to reduce consecutive repetition.

It also uses `platform_rules.csv`, `posting_time_windows.csv` and the campaign structure data when selecting the publishing plan.

## How Excel export works

The exporter creates:

1. Social Media Calendar
2. Campaign Overview
3. Content Bucket Distribution
4. Persona Distribution
5. Posting Schedule

The workbook uses `openpyxl`.

## How the scheduler works

The scheduler stores data in `output/scheduled_posts.csv`.

It can:
- Schedule a post
- Change its date/time
- Cancel a scheduled post
- Mark a post as Published
- Identify due Scheduled posts as Ready to Publish
- View upcoming posts

The scheduler does not publish directly to social platforms.

## Campaign history

Generated campaigns go into `output/campaign_history.csv`.

## Demo / testing

Run:

```bash
python demo.py
```

The demo checks:
- Lip gloss
- Lip oil
- Lipstick
- Lip mask
- Lip balm
- An unknown product

It prints persona, bucket, platform, image title and posting information for sample generated campaigns.

## Known limitations

- The application does not connect to social-media APIs.
- It does not publish posts.
- Content generation uses deterministic local templates and data rather than an online generative AI model.
- Unknown products receive temporary profiles rather than being added to the permanent catalogue.
- Posting times come from the supplied fictional planning dataset and do not guarantee performance.
- The current version has no graphical UI.
