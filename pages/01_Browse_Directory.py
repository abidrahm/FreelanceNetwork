import streamlit as st
import pandas as pd
from data_manager import get_listings_by_category, get_categories
from utils import track_page_view, apply_page_styling

# Page configuration
st.set_page_config(
    page_title="Browse Directory",
    page_icon="🔍",
    layout="wide"
)

# Apply consistent styling across the app
apply_page_styling()

# Add page-specific styles
st.markdown("""
<style>
    /* Listing card styling */
    .listing-card {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        background-color: #FFFFFF;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .listing-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
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
</style>
""", unsafe_allow_html=True)

# Get selected category from session state
selected_category = None
if 'selected_category' in st.session_state:
    selected_category = st.session_state['selected_category']

# Title and description
st.title("Browse Directory")
st.write("Explore businesses by category")

# Sidebar with categories
st.sidebar.title("Categories")
categories = get_categories()

# Allow selection of category from sidebar
for i, category in enumerate(categories['name']):
    if st.sidebar.button(category, key=f"cat_sidebar_{i}"):
        selected_category = category
        st.session_state['selected_category'] = category
        st.rerun()

# Display listings for selected category
if selected_category:
    st.header(f"{selected_category} Businesses")
    
    # Get listings for this category
    listings = get_listings_by_category(selected_category)
    
    if listings.empty:
        st.info(f"No businesses listed in {selected_category} yet.")
    else:
        # Display listings in a grid with modern cards
        cols = st.columns(3)
        
        for i, row in listings.iterrows():
            with cols[i % 3]:
                # Create a styled card for each listing
                st.markdown(f"""
                <div class="listing-card">
                    <h3>{row['name']}</h3>
                    <p><em>📍 {row['location']}</em></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Description with truncation for long text
                description = row['description']
                if len(description) > 150:
                    description = description[:150] + "..."
                st.write(description)
                
                # Use columns for buttons with better styling
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button("View Details", key=f"view_{row['id']}", use_container_width=True):
                        # Track the page view
                        track_page_view(row['id'])
                        
                        # Store in session state
                        st.session_state['current_listing'] = row['id']
                        
                        # Display details
                        st.session_state['show_details'] = True
                        st.rerun()
                
                with btn_col2:
                    # Style the website link as a button for consistency
                    st.markdown(f"""
                    <a href="{row['website']}" target="_blank" style="
                        display: inline-block;
                        width: 100%;
                        padding: 0.5rem 1rem;
                        background-color: #F8F9FA;
                        color: #212529;
                        text-align: center;
                        text-decoration: none;
                        font-size: 16px;
                        border-radius: 4px;
                        border: 1px solid #e0e0e0;
                        cursor: pointer;
                    ">Visit Website</a>
                    """, unsafe_allow_html=True)
                
                # Add some spacing instead of a line
                st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)
else:
    # If no category selected, show a prompt to select
    st.info("Please select a category from the sidebar to browse businesses.")
    
    # Show a preview of categories
    st.subheader("Popular Categories")
    cols = st.columns(4)
    
    for i, category in enumerate(categories['name'][:8]):  # Show first 8 categories
        with cols[i % 4]:
            if st.button(category, key=f"cat_preview_{i}"):
                selected_category = category
                st.session_state['selected_category'] = category
                st.rerun()

# Detail view for a specific listing
if 'show_details' in st.session_state and st.session_state['show_details'] and 'current_listing' in st.session_state:
    from data_manager import get_listing_by_id
    
    listing_id = st.session_state['current_listing']
    listing = get_listing_by_id(listing_id)
    
    if listing is not None:
        # Create a modern detailed view with styling
        st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
        
        # Header with name and category
        st.markdown(f"""
        <div style="background-color: #F8F9FA; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #4361EE;">
            <h1 style="margin-bottom: 5px;">{listing['name']}</h1>
            <p style="font-size: 18px; color: #6c757d;"><strong>Category:</strong> {listing['category']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Main content in two columns
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Description and details
            st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0; margin-bottom: 20px;">
                <h3 style="color: #4361EE; margin-bottom: 15px;">About This Business</h3>
            """, unsafe_allow_html=True)
            st.write(listing['description'])
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Contact information in a styled card
            st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0;">
                <h3 style="color: #4361EE; margin-bottom: 15px;">Contact Information</h3>
            """, unsafe_allow_html=True)
            
            st.write(f"📍 **Location:** {listing['location']}")
            st.write(f"📧 **Email:** {listing['email']}")
            st.write(f"📞 **Phone:** {listing['phone']}")
            
            # Website button
            st.markdown(f"""
            <a href="{listing['website']}" target="_blank" style="
                display: inline-block;
                margin-top: 15px;
                padding: 10px 20px;
                background-color: #4361EE;
                color: white;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                border-radius: 4px;
                border: none;
                cursor: pointer;
            ">Visit Website</a>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            # Business stats in a styled card
            st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0; margin-bottom: 20px;">
                <h3 style="color: #4361EE; margin-bottom: 15px;">Business Stats</h3>
            """, unsafe_allow_html=True)
            
            # Get view count
            from utils import get_listing_views
            views = get_listing_views(listing_id)
            
            st.metric("Page Views", views)
            st.write(f"**Listed since:** {listing['submitted_date']}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Close button with better styling
            if st.button("← Back to Listings", key="close_details", use_container_width=True):
                st.session_state['show_details'] = False
                st.rerun()
            
            # Call to action for premium
            st.markdown("""
            <div style="background-color: #F0F3FF; padding: 15px; border-radius: 10px; margin-top: 20px; text-align: center;">
                <h4 style="color: #4361EE;">Is this your business?</h4>
                <p>Upgrade to premium to enhance your listing visibility and track detailed analytics.</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Explore Premium Options", key="premium_cta", use_container_width=True):
                st.switch_page("pages/04_Premium_Options.py")
