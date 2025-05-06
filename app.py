import streamlit as st
import pandas as pd
import os
from datetime import datetime
from data_manager import initialize_data, get_premium_listings, get_listings_by_category, get_categories
from utils import track_page_view

# Setup page config
st.set_page_config(
    page_title="Business Directory",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize data if it doesn't exist
initialize_data()

# Sidebar
st.sidebar.title("Directory Navigation")
st.sidebar.write("Find businesses or submit your own listing")

# Main content
st.title("Business Directory")
st.subheader("Discover top businesses in your area")

# Display featured/premium listings
st.header("Featured Businesses")
premium_listings = get_premium_listings()

if not premium_listings.empty:
    # Display premium listings in a more prominent way
    for i, row in premium_listings.iterrows():
        col1, col2 = st.columns([1, 3])
        with col1:
            st.subheader(f"⭐ {row['name']}")
            st.caption(f"Category: {row['category']}")
        with col2:
            st.write(row['description'])
            st.write(f"📍 {row['location']}")
            st.write(f"🔗 [{row['website']}]({row['website']})")
            
            # Track view when user clicks "View Details"
            if st.button(f"View Details 👁️", key=f"premium_{i}"):
                track_page_view(row['id'], "premium")
                st.session_state['current_listing'] = row['id']
                st.rerun()
else:
    st.info("No premium listings available yet.")

# Display category selection
st.header("Browse by Category")
categories = get_categories()
col1, col2, col3 = st.columns(3)

category_cols = [col1, col2, col3]
for i, category in enumerate(categories['name']):
    if category_cols[i % 3].button(category, use_container_width=True):
        # Store selected category in session state
        st.session_state['selected_category'] = category
        # Navigate to browse page
        st.switch_page("pages/01_Browse_Directory.py")

# Call to action
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.header("Add Your Business")
    st.write("Get your business listed in our directory.")
    if st.button("Submit a Listing", use_container_width=True):
        st.switch_page("pages/03_Submit_Listing.py")

with col2:
    st.header("Premium Placement")
    st.write("Increase visibility with our premium options.")
    if st.button("Explore Premium Options", use_container_width=True):
        st.switch_page("pages/04_Premium_Options.py")

# Footer
st.markdown("---")
st.write("© 2023 Business Directory | [Terms of Service](https://example.com/terms) | [Privacy Policy](https://example.com/privacy)")
