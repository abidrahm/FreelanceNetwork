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

# Custom CSS to enhance styling
st.markdown("""
<style>
    /* Card styling for listings */
    div.stButton > button:first-child {
        background-color: #4361EE;
        color: white;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        border: none;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
    }
    div.stButton > button:hover {
        background-color: #3A56D4;
    }
    
    /* Header styling */
    h1, h2, h3, h4 {
        font-family: 'sans-serif';
        font-weight: 600;
        color: #212529;
    }
    h1 {
        border-bottom: 2px solid #4361EE;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    /* Premium listing style */
    .premium-card {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        background-color: #FAFBFF;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* Category button styling */
    .category-button {
        background-color: #F8F9FA;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        margin-bottom: 15px;
        transition: transform 0.2s;
    }
    .category-button:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Footer styling */
    .footer {
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #e0e0e0;
        text-align: center;
        color: #6c757d;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize data if it doesn't exist
initialize_data()

# Sidebar with improved styling
st.sidebar.title("Directory Navigation")
st.sidebar.markdown("---")
st.sidebar.markdown("### Find Business Solutions")
st.sidebar.write("Discover top-rated businesses or submit your listing today.")

# Main content
st.title("Business Directory")
st.subheader("Discover top businesses in your area")

# Display featured/premium listings
st.header("Featured Businesses")
premium_listings = get_premium_listings()

if not premium_listings.empty:
    # Display premium listings in a more prominent way
    for i, row in premium_listings.iterrows():
        # Use premium card styling
        st.markdown(f"""
        <div class="premium-card">
            <h3>⭐ {row['name']}</h3>
            <p><em>Category: {row['category']}</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(row['description'])
            st.write(f"📍 {row['location']}")
            st.write(f"🔗 [{row['website']}]({row['website']})")
        
        with col2:
            # Track view when user clicks "View Details"
            if st.button(f"View Details 👁️", key=f"premium_{i}", use_container_width=True):
                track_page_view(row['id'], "premium")
                st.session_state['current_listing'] = row['id']
                st.rerun()
else:
    st.info("No premium listings available yet.")

# Display category selection with modern cards
st.header("Browse by Category")
categories = get_categories()

# Display categories in a grid with styled cards
st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

category_cols = [col1, col2, col3, col4]
for i, category in enumerate(categories['name']):
    with category_cols[i % 4]:
        # Add some icons based on category name
        icon = "🍽️"  # Default icon
        if "Restaurant" in category:
            icon = "🍽️"
        elif "Retail" in category:
            icon = "🛍️"
        elif "Services" in category:
            icon = "🔧"
        elif "Health" in category:
            icon = "💆"
        elif "Tech" in category:
            icon = "💻"
        elif "Home" in category:
            icon = "🏠"
        elif "Education" in category:
            icon = "📚"
        elif "Entertainment" in category:
            icon = "🎭"
        
        # Create a styled category card
        st.markdown(f"""
        <div class="category-button">
            <h3 style="text-align: center; font-size: 24px;">{icon}</h3>
            <h4 style="text-align: center; margin-top: 5px;">{category}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"Browse {category}", key=f"cat_{i}", use_container_width=True):
            # Store selected category in session state
            st.session_state['selected_category'] = category
            # Navigate to browse page
            st.switch_page("pages/01_Browse_Directory.py")

# Call to action section with enhanced styling
st.markdown("---")
st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>Grow Your Business With Us</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div style="background-color: #F8F9FA; padding: 20px; border-radius: 10px; height: 100%;">
        <h3 style="color: #4361EE;">Add Your Business</h3>
        <p>Get your business listed in our directory and reach new customers today.</p>
        <ul>
            <li>Increase your online visibility</li>
            <li>Connect with targeted customers</li>
            <li>Build your business credibility</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Submit a Listing", use_container_width=True):
        st.switch_page("pages/03_Submit_Listing.py")

with col2:
    st.markdown("""
    <div style="background-color: #F8F9FA; padding: 20px; border-radius: 10px; height: 100%;">
        <h3 style="color: #4361EE;">Premium Placement</h3>
        <p>Stand out from competitors with premium listing options.</p>
        <ul>
            <li>Featured placement on homepage</li>
            <li>Priority in search results</li>
            <li>Enhanced listing with additional details</li>
            <li>Analytics dashboard access</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explore Premium Options", use_container_width=True):
        st.switch_page("pages/04_Premium_Options.py")

# Modern footer with better styling
st.markdown("---")
st.markdown("""
<div class="footer">
    <div style="display: flex; justify-content: center; gap: 30px; margin-bottom: 20px;">
        <div>
            <h4>About Us</h4>
            <p>We connect businesses with customers</p>
        </div>
        <div>
            <h4>Quick Links</h4>
            <p><a href="pages/01_Browse_Directory.py">Browse Directory</a> | 
            <a href="pages/02_Search.py">Search</a> | 
            <a href="pages/03_Submit_Listing.py">Add Listing</a></p>
        </div>
        <div>
            <h4>Contact</h4>
            <p>info@businessdirectory.com</p>
        </div>
    </div>
    <p>© 2023 Business Directory | <a href="https://example.com/terms">Terms of Service</a> | <a href="https://example.com/privacy">Privacy Policy</a></p>
</div>
""", unsafe_allow_html=True)
