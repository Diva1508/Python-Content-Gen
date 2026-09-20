from __future__ import annotations
from pathlib import Path
import pandas as pd

REQUIRED_FILES = [
    "brand_profile.csv","product_catalogue.csv","ingredient_library.csv",
    "flavour_library.csv","customer_personas.csv","content_buckets.csv",
    "platform_rules.csv","posting_time_windows.csv","content_templates.csv",
    "hook_library.csv","cta_library.csv","hashtag_meta_library.csv",
    "image_style_library.csv","alt_text_rules.csv","image_title_rules.csv",
    "campaign_structure.csv","dataset_index.csv","dataset_field_dictionary.csv"
]

class DataLoadError(Exception):
    pass

class DataStore:
    def __init__(self, data_dir: str | Path):
        self.data_dir=Path(data_dir)
        self.tables={}
        self.load_all()

    def load_all(self):
        missing=[f for f in REQUIRED_FILES if not (self.data_dir/f).exists()]
        if missing:
            raise DataLoadError("Missing CSV files: " + ", ".join(missing))
        for filename in REQUIRED_FILES:
            try:
                df=pd.read_csv(self.data_dir/filename, dtype=str, keep_default_na=False)
            except Exception as exc:
                raise DataLoadError(f"Could not read {filename}: {exc}") from exc
            if df.columns.duplicated().any():
                raise DataLoadError(f"Duplicate columns found in {filename}.")
            self.tables[filename]=df
        self._validate_ids()

    def _validate_ids(self):
        id_columns={
            "product_catalogue.csv":"Product ID","ingredient_library.csv":"Ingredient ID",
            "flavour_library.csv":"Flavour ID","customer_personas.csv":"Persona ID",
            "content_buckets.csv":"Bucket ID","content_templates.csv":"Template ID",
            "hook_library.csv":"Hook ID","cta_library.csv":"CTA ID","image_style_library.csv":"Image ID",
            "alt_text_rules.csv":"Rule ID","image_title_rules.csv":"Rule ID",
            "campaign_structure.csv":"Campaign Row ID","posting_time_windows.csv":"Time ID"
        }
        for file,col in id_columns.items():
            df=self.tables[file]
            if col not in df.columns:
                raise DataLoadError(f"{file} is missing required column: {col}")
            vals=df[col].astype(str).str.strip()
            if vals.eq("").any(): raise DataLoadError(f"{file} contains empty IDs in {col}.")
            if vals.duplicated().any(): raise DataLoadError(f"{file} contains duplicate IDs in {col}.")

    def get(self, filename: str) -> pd.DataFrame:
        return self.tables[filename].copy()

    def brand(self): return self.get("brand_profile.csv").iloc[0].to_dict()
    def products(self): return self.get("product_catalogue.csv")
    def ingredients(self): return self.get("ingredient_library.csv")
    def flavours(self): return self.get("flavour_library.csv")
    def personas(self): return self.get("customer_personas.csv")
    def buckets(self): return self.get("content_buckets.csv")
    def platforms(self): return self.get("platform_rules.csv")
    def times(self): return self.get("posting_time_windows.csv")
    def templates(self): return self.get("content_templates.csv")
    def hooks(self): return self.get("hook_library.csv")
    def ctas(self): return self.get("cta_library.csv")
    def hashtags(self): return self.get("hashtag_meta_library.csv")
    def images(self): return self.get("image_style_library.csv")
    def alt_rules(self): return self.get("alt_text_rules.csv")
    def title_rules(self): return self.get("image_title_rules.csv")
    def campaign_structure(self): return self.get("campaign_structure.csv")
