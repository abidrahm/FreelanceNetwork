import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from data_manager import get_analytics_data, get_listing_by_id
from utils import verify_admin

# Page configuration
st.set_page_config(
    page_title="Directory Analytics",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("Directory Analytics")

# Check if admin is logged in
if 'admin_logged_in' not in st.session_state or not st.session_state['admin_logged_in']:
    st.warning("You need to be logged in as an admin to view analytics.")
    
    with st.form("login_form"):
        st.write("Please enter your admin credentials")
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        submit = st.form_submit_button("Login")
        
        if submit:
            if verify_admin(username, password):
                st.session_state['admin_logged_in'] = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    # Return to main site
    if st.button("Return to Main Site"):
        st.switch_page("app.py")
else:
    # Get analytics data
    analytics_data = get_analytics_data()
    
    if analytics_data.empty:
        st.info("No analytics data available yet. As users interact with listings, data will appear here.")
    else:
        # Convert timestamp to datetime
        analytics_data["timestamp"] = pd.to_datetime(analytics_data["timestamp"])
        
        # Date filter
        st.subheader("Filter Data")
        col1, col2 = st.columns(2)
        
        with col1:
            # Default to last 30 days
            default_start = datetime.now() - timedelta(days=30)
            start_date = st.date_input(
                "Start Date",
                default_start,
                max_value=datetime.now()
            )
        
        with col2:
            end_date = st.date_input(
                "End Date",
                datetime.now(),
                max_value=datetime.now()
            )
        
        # Filter by date
        filtered_data = analytics_data[
            (analytics_data["timestamp"].dt.date >= start_date) &
            (analytics_data["timestamp"].dt.date <= end_date)
        ]
        
        if filtered_data.empty:
            st.info("No data available for the selected date range.")
        else:
            # Overview metrics
            st.header("Overview")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_views = len(filtered_data)
                st.metric("Total Page Views", total_views)
            
            with col2:
                unique_listings = filtered_data["listing_id"].nunique()
                st.metric("Listings Viewed", unique_listings)
            
            with col3:
                premium_views = len(filtered_data[filtered_data["listing_type"] == "premium"])
                premium_percentage = (premium_views / total_views) * 100 if total_views > 0 else 0
                st.metric("Premium Listing Views", f"{premium_views} ({premium_percentage:.1f}%)")
            
            # Views over time
            st.header("Views Over Time")
            
            # Group by day
            daily_views = filtered_data.groupby(filtered_data["timestamp"].dt.date).size().reset_index()
            daily_views.columns = ["Date", "Views"]
            
            # Create line chart
            fig = px.line(
                daily_views, 
                x="Date", 
                y="Views",
                title="Daily Page Views",
                labels={"Date": "Date", "Views": "Number of Views"}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Views by listing type
            st.header("Premium vs. Standard Views")
            
            # Group by listing type
            type_views = filtered_data.groupby("listing_type").size().reset_index()
            type_views.columns = ["Listing Type", "Views"]
            
            # Create pie chart
            fig = px.pie(
                type_views, 
                values="Views", 
                names="Listing Type",
                title="Views by Listing Type",
                color_discrete_map={"premium": "#FFD700", "standard": "#1E90FF"}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Top listings table
            st.header("Top Performing Listings")
            
            # Group by listing ID
            top_listings = filtered_data.groupby("listing_id").size().reset_index()
            top_listings.columns = ["Listing ID", "Views"]
            top_listings = top_listings.sort_values("Views", ascending=False).head(10)
            
            # Add listing details
            top_listings["Listing Name"] = top_listings["Listing ID"].apply(
                lambda x: get_listing_by_id(x)["name"] if get_listing_by_id(x) is not None else "Unknown"
            )
            
            top_listings["Category"] = top_listings["Listing ID"].apply(
                lambda x: get_listing_by_id(x)["category"] if get_listing_by_id(x) is not None else "Unknown"
            )
            
            top_listings["Type"] = top_listings["Listing ID"].apply(
                lambda x: "Premium" if x in filtered_data[filtered_data["listing_type"] == "premium"]["listing_id"].unique() else "Standard"
            )
            
            # Reorder columns for display
            top_listings = top_listings[["Listing Name", "Category", "Type", "Views", "Listing ID"]]
            
            # Display table
            st.dataframe(top_listings, use_container_width=True)
            
            # Daily breakdown
            st.header("Daily Breakdown")
            
            # Create date slider
            date_list = sorted(filtered_data["timestamp"].dt.date.unique())
            if len(date_list) > 1:
                selected_date = st.select_slider(
                    "Select Date to View Detailed Breakdown",
                    options=date_list,
                    value=date_list[-1]  # Default to most recent date
                )
                
                # Filter for selected date
                date_data = filtered_data[filtered_data["timestamp"].dt.date == selected_date]
                
                # Hourly breakdown
                st.subheader(f"Hourly Breakdown for {selected_date}")
                
                # Group by hour
                hourly_data = date_data.groupby(date_data["timestamp"].dt.hour).size().reset_index()
                hourly_data.columns = ["Hour", "Views"]
                
                # Create bar chart
                fig = px.bar(
                    hourly_data, 
                    x="Hour", 
                    y="Views",
                    title=f"Views by Hour on {selected_date}",
                    labels={"Hour": "Hour of Day", "Views": "Number of Views"}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Export option
            st.subheader("Export Data")
            
            if st.button("Export to CSV"):
                # Convert to CSV
                csv = filtered_data.to_csv(index=False).encode('utf-8')
                
                # Create download button
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"directory_analytics_{start_date}_to_{end_date}.csv",
                    mime="text/csv"
                )

    # Return to admin dashboard
    if st.button("Return to Admin Dashboard"):
        st.switch_page("pages/05_Admin_Login.py")
