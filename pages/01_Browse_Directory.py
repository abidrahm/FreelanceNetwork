import streamlit as st
import pandas as pd
from data_manager import get_listings_by_category, get_categories
from utils import track_page_view

# Page configuration
st.set_page_config(
    page_title="Browse Directory",
    page_icon="🔍",
    layout="wide"
)

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
        # Display listings in a grid
        cols = st.columns(3)
        
        for i, row in listings.iterrows():
            with cols[i % 3]:
                with st.container():
                    st.subheader(row['name'])
                    st.write(row['description'][:150] + "..." if len(row['description']) > 150 else row['description'])
                    st.write(f"📍 {row['location']}")
                    
                    # Use columns for buttons
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        if st.button("View Details", key=f"view_{row['id']}"):
                            # Track the page view
                            track_page_view(row['id'])
                            
                            # Store in session state
                            st.session_state['current_listing'] = row['id']
                            
                            # Display details
                            st.session_state['show_details'] = True
                            st.rerun()
                    
                    with btn_col2:
                        st.markdown(f"[Visit Website]({row['website']})")
                    
                    # Add some visual separation
                    st.markdown("---")
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
        # Create a modal-like experience with a full card
        st.markdown("---")
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.title(listing['name'])
                st.subheader(f"Category: {listing['category']}")
                st.write(listing['description'])
                
                st.markdown("### Contact Information")
                st.write(f"📍 **Location:** {listing['location']}")
                st.write(f"📧 **Email:** {listing['email']}")
                st.write(f"📞 **Phone:** {listing['phone']}")
                st.write(f"🔗 **Website:** [{listing['website']}]({listing['website']})")
            
            with col2:
                st.markdown("### Business Details")
                
                # Get view count
                from utils import get_listing_views
                views = get_listing_views(listing_id)
                
                st.metric("Page Views", views)
                st.write(f"Listed since: {listing['submitted_date']}")
                
                if st.button("Close Details", key="close_details"):
                    st.session_state['show_details'] = False
                    st.rerun()
