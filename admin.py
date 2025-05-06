import streamlit as st
import pandas as pd
from data_manager import (
    get_all_listings, 
    approve_listing,
    delete_listing,
    get_analytics_data,
    get_listing_by_id
)
import plotly.express as px
from datetime import datetime, timedelta

def render_admin_dashboard():
    """Render the admin dashboard."""
    st.title("Admin Dashboard")
    
    # Admin tabs
    tab1, tab2, tab3 = st.tabs(["Listing Management", "Analytics", "Settings"])
    
    with tab1:
        render_listing_management()
    
    with tab2:
        render_analytics()
    
    with tab3:
        render_settings()

def render_listing_management():
    """Render the listing management section."""
    st.header("Listing Management")
    
    # Get all listings including unapproved ones
    listings = get_all_listings(approved_only=False)
    
    if listings.empty:
        st.info("No listings available.")
        return
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        filter_status = st.selectbox(
            "Filter by Status", 
            ["All", "Approved", "Pending"]
        )
    
    with col2:
        categories = listings["category"].unique()
        filter_category = st.selectbox(
            "Filter by Category",
            ["All"] + list(categories)
        )
    
    # Apply filters
    filtered_listings = listings.copy()
    
    if filter_status == "Approved":
        filtered_listings = filtered_listings[filtered_listings["approved"] == True]
    elif filter_status == "Pending":
        filtered_listings = filtered_listings[filtered_listings["approved"] == False]
    
    if filter_category != "All":
        filtered_listings = filtered_listings[filtered_listings["category"] == filter_category]
    
    # Display listings with actions
    for i, row in filtered_listings.iterrows():
        with st.expander(f"{row['name']} - {row['category']} - {'✅ Approved' if row['approved'] else '⏳ Pending'}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Description:** {row['description']}")
                st.write(f"**Website:** [{row['website']}]({row['website']})")
                st.write(f"**Contact:** {row['email']} | {row['phone']}")
                st.write(f"**Location:** {row['location']}")
                st.write(f"**Submitted:** {row['submitted_date']}")
            
            with col2:
                if not row['approved']:
                    if st.button("Approve", key=f"approve_{row['id']}"):
                        approve_listing(row['id'])
                        st.success("Listing approved!")
                        st.rerun()
                
                if st.button("Delete", key=f"delete_{row['id']}"):
                    delete_listing(row['id'])
                    st.success("Listing deleted!")
                    st.rerun()

def render_analytics():
    """Render the analytics section."""
    st.header("Analytics Dashboard")
    
    analytics_data = get_analytics_data()
    
    if analytics_data.empty:
        st.info("No analytics data available yet.")
        return
    
    # Convert timestamp to datetime
    analytics_data["timestamp"] = pd.to_datetime(analytics_data["timestamp"])
    
    # Date filter
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            datetime.now() - timedelta(days=30)
        )
    
    with col2:
        end_date = st.date_input(
            "End Date",
            datetime.now()
        )
    
    # Filter by date
    filtered_data = analytics_data[
        (analytics_data["timestamp"].dt.date >= start_date) &
        (analytics_data["timestamp"].dt.date <= end_date)
    ]
    
    if filtered_data.empty:
        st.info("No data available for the selected date range.")
        return
    
    # Total views
    st.metric("Total Page Views", len(filtered_data))
    
    # Views by day
    daily_views = filtered_data.groupby(filtered_data["timestamp"].dt.date).size().reset_index()
    daily_views.columns = ["Date", "Views"]
    
    fig1 = px.line(
        daily_views, 
        x="Date", 
        y="Views",
        title="Page Views Over Time"
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Views by listing type
    type_views = filtered_data.groupby("listing_type").size().reset_index()
    type_views.columns = ["Listing Type", "Views"]
    
    fig2 = px.pie(
        type_views, 
        values="Views", 
        names="Listing Type",
        title="Views by Listing Type"
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # Top listings
    st.subheader("Top Listings by Views")
    top_listings = filtered_data.groupby("listing_id").size().reset_index()
    top_listings.columns = ["Listing ID", "Views"]
    top_listings = top_listings.sort_values("Views", ascending=False).head(10)
    
    # Add listing names
    top_listings["Listing Name"] = top_listings["Listing ID"].apply(
        lambda x: get_listing_by_id(x)["name"] if get_listing_by_id(x) is not None else "Unknown"
    )
    
    st.dataframe(
        top_listings[["Listing Name", "Views", "Listing ID"]], 
        use_container_width=True,
        hide_index=True
    )

def render_settings():
    """Render the settings section."""
    st.header("Directory Settings")
    
    st.subheader("Monetization Settings")
    
    # Premium package settings
    st.write("### Premium Package Pricing")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.number_input("Basic Package ($)", value=29, key="basic_price")
        st.write("Features:")
        st.write("- Higher placement in listings")
        st.write("- 30 days premium visibility")
    
    with col2:
        st.number_input("Standard Package ($)", value=49, key="standard_price")
        st.write("Features:")
        st.write("- Featured on category pages")
        st.write("- 60 days premium visibility")
        st.write("- Enhanced listing details")
    
    with col3:
        st.number_input("Premium Package ($)", value=99, key="premium_price")
        st.write("Features:")
        st.write("- Featured on homepage")
        st.write("- 90 days premium visibility")
        st.write("- Enhanced listing details")
        st.write("- Featured in search results")
    
    # Save settings button (in a real app, this would save to a database or config file)
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")
