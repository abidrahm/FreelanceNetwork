import streamlit as st
import pandas as pd
from data_manager import search_listings
from utils import track_page_view

# Page configuration
st.set_page_config(
    page_title="Search Directory",
    page_icon="🔍",
    layout="wide"
)

# Title and description
st.title("Search Business Directory")
st.write("Find businesses by name, category, or keywords")

# Search form
with st.form(key="search_form"):
    search_query = st.text_input("Search for businesses", placeholder="Enter business name, category, or keywords")
    submit_button = st.form_submit_button("Search", use_container_width=True)

# Process search when form is submitted
if submit_button and search_query:
    # Get search results
    results = search_listings(search_query)
    
    # Display results
    st.header(f"Search Results for '{search_query}'")
    
    if results.empty:
        st.info("No results found. Try different keywords.")
    else:
        st.write(f"Found {len(results)} results")
        
        # Display results in a grid
        cols = st.columns(2)
        
        for i, row in results.iterrows():
            with cols[i % 2]:
                with st.container():
                    st.subheader(row['name'])
                    st.caption(f"Category: {row['category']}")
                    st.write(row['description'][:150] + "..." if len(row['description']) > 150 else row['description'])
                    st.write(f"📍 {row['location']}")
                    
                    # Use columns for buttons
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        if st.button("View Details", key=f"view_{row['id']}"):
                            # Track the page view
                            track_page_view(row['id'])
                            
                            # Store in session state and show details
                            st.session_state['current_listing'] = row['id']
                            st.session_state['show_details'] = True
                            st.rerun()
                    
                    with btn_col2:
                        st.markdown(f"[Visit Website]({row['website']})")
                    
                    # Add some visual separation
                    st.markdown("---")
elif submit_button:
    st.warning("Please enter a search term.")

# Search tips
with st.expander("Search Tips"):
    st.write("""
    - Search by business name: "Joe's Coffee Shop"
    - Search by category: "Restaurant" or "Tech"
    - Search by location: "Downtown" or "New York"
    - Search by keywords in description: "organic" or "professional"
    """)

# Detail view for a specific listing (same as in Browse page)
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
