import streamlit as st

from data_loader import load_all_data
from product_matcher import match_product
from persona_selector import select_persona
from content_planner import create_campaign_plan
from content_generator import generate_content

st.title("Beauty & Skincare Social Media Campaign Generator")

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
    ["Instagram", "Facebook", "LinkedIn", "Pinterest", "X"],
    default=["Instagram", "LinkedIn"]
)

if st.button("Generate Campaign"):

    if not product_name:
        st.error("Please enter a product name.")

    elif not benefits:
        st.error("Please enter product benefits.")

    else:
        with st.spinner("Generating your campaign..."):

            data = load_all_data()

            product = match_product(
                product_name,
                benefits,
                data
            )

            campaign = create_campaign_plan(
                product=product,
                duration=duration,
                platforms=platforms,
                data=data
            )

        st.success("Campaign generated successfully!")

        st.dataframe(campaign)
