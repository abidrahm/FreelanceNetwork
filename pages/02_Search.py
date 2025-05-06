import streamlit as st
import pandas as pd
from data_manager import search_listings
from utils import track_page_view, apply_page_styling

# Page configuration
st.set_page_config(
    page_title="Search Directory",
    page_icon="🔍",
    layout="wide"
)

# Apply consistent styling across the app
apply_page_styling()

# Add page-specific styles
st.markdown("""
<style>
    /* Search result card styling */
    .search-result {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        background-color: #FFFFFF;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .search-result:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Search form styling */
    .search-form {
        background-color: #F8F9FA;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("Search Business Directory")
st.write("Find businesses by name, category, or keywords")

# Search form with improved styling
st.markdown('<div class="search-form">', unsafe_allow_html=True)
with st.form(key="search_form"):
    st.markdown("<h3>Find the perfect business</h3>", unsafe_allow_html=True)
    search_query = st.text_input("Search for businesses", placeholder="Enter business name, category, or keywords")
    submit_button = st.form_submit_button("Search", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

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
        
        # Display results in a grid with modern styling
        cols = st.columns(2)
        
        for i, row in results.iterrows():
            with cols[i % 2]:
                # Create a styled card for each search result
                st.markdown(f"""
                <div class="search-result">
                    <h3>{row['name']}</h3>
                    <p><em>Category: {row['category']}</em></p>
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
                        
                        # Store in session state and show details
                        st.session_state['current_listing'] = row['id']
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
                
                # Add some spacing
                st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)
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

# Detail view for a specific listing with enhanced styling
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
            if st.button("← Back to Results", key="close_details", use_container_width=True):
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
