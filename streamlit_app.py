from __future__ import annotations
from pathlib import Path
from datetime import date

import streamlit as st

from data_loader import DataStore, DataLoadError
from product_matcher import match_product
from calendar_generator import generate_calendar
from utils import new_campaign_id

BASE_DIR = Path(__file__).resolve().parent


@st.cache_resource
def get_store():
    return DataStore(BASE_DIR)


st.title("Beauty & Skincare Social Media Campaign Generator")

try:
    store = get_store()
except DataLoadError as exc:
    st.error(f"Data loading error: {exc}")
    st.stop()

available_platforms = store.platforms()["Platform"].tolist()
default_platforms = [p for p in ("Instagram", "LinkedIn") if p in available_platforms]

product_name = st.text_input("Product Name")

benefits = st.text_area(
    "Product Benefits",
    placeholder="Enter the main benefits of the product"
)

duration = st.selectbox(
    "Campaign Duration",
    [7, 14, 30]
)

platforms = st.multiselect(
    "Platforms",
    available_platforms,
    default=default_platforms
)

if st.button("Generate Campaign"):

    if not product_name:
        st.error("Please enter a product name.")

    elif not benefits:
        st.error("Please enter product benefits.")

    elif not platforms:
        st.error("Please select at least one platform.")

    else:
        with st.spinner("Generating your campaign..."):
            product = match_product(product_name, benefits, store)
            campaign = generate_calendar(
                product,
                duration,
                store,
                platforms,
                date.today(),
                new_campaign_id(),
            )

        st.success("Campaign generated successfully!")
        st.dataframe(campaign)
