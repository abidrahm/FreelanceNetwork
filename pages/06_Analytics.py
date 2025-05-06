import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from data_manager import get_analytics_data, get_listing_by_id
from utils import verify_admin, apply_page_styling

# Page configuration
st.set_page_config(
    page_title="Directory Analytics",
    page_icon="📊",
    layout="wide"
)

# Apply consistent styling across the app
apply_page_styling()

# Add page-specific styles
st.markdown("""
<style>
    /* Analytics card styling */
    .analytics-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Stat counter styling */
    .stat-counter {
        background-color: #F8F9FA;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        border-left: 4px solid #4361EE;
    }
    
    /* Login form styling */
    .login-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 30px;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("Directory Analytics")

# Check if admin is logged in
if 'admin_logged_in' not in st.session_state or not st.session_state['admin_logged_in']:
    st.warning("You need to be logged in as an admin to view analytics.")
    
    # Create a centered login container
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Login form with styled header
        st.markdown('<h3 style="color: #4361EE; margin-bottom: 20px; text-align: center;">Admin Access</h3>', unsafe_allow_html=True)
        
        # Admin icon
        st.markdown('<div style="text-align: center; margin-bottom: 20px;"><img src="https://cdn-icons-png.flaticon.com/512/1077/1077114.png" width="80"></div>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("<p style='text-align: center;'>Please enter your admin credentials to view analytics</p>", unsafe_allow_html=True)
            
            username = st.text_input("Username", placeholder="Enter admin username")
            password = st.text_input("Password", type="password", placeholder="Enter admin password")
            
            # Add some spacing
            st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
            
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if verify_admin(username, password):
                    st.session_state['admin_logged_in'] = True
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        # Help text
        st.info("For demonstration, use username 'admin' and password 'directory_admin'")
        
        # Return to main site
        st.markdown("<div style='text-align: center; margin-top: 15px;'>", unsafe_allow_html=True)
        if st.button("Return to Main Site"):
            st.switch_page("app.py")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # Get analytics data
    analytics_data = get_analytics_data()
    
    if analytics_data.empty:
        st.info("No analytics data available yet. As users interact with listings, data will appear here.")
    else:
        # Convert timestamp to datetime
        analytics_data["timestamp"] = pd.to_datetime(analytics_data["timestamp"])
        
        # Date filter in a styled card
        st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
        st.markdown("<h3>Filter Data</h3>", unsafe_allow_html=True)
        
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
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Filter by date
        filtered_data = analytics_data[
            (analytics_data["timestamp"].dt.date >= start_date) &
            (analytics_data["timestamp"].dt.date <= end_date)
        ]
        
        if filtered_data.empty:
            st.info("No data available for the selected date range.")
        else:
            # Overview metrics with enhanced styling
            st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
            st.markdown("<h3>Overview</h3>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_views = len(filtered_data)
                st.markdown(f"""
                <div class="stat-counter">
                    <h4 style="margin-bottom: 5px;">Total Page Views</h4>
                    <h2 style="color: #4361EE; margin: 0;">{total_views}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                unique_listings = filtered_data["listing_id"].nunique()
                st.markdown(f"""
                <div class="stat-counter" style="border-left-color: #2EC4B6;">
                    <h4 style="margin-bottom: 5px;">Listings Viewed</h4>
                    <h2 style="color: #2EC4B6; margin: 0;">{unique_listings}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                premium_views = len(filtered_data[filtered_data["listing_type"] == "premium"])
                premium_percentage = (premium_views / total_views) * 100 if total_views > 0 else 0
                st.markdown(f"""
                <div class="stat-counter" style="border-left-color: #FF5722;">
                    <h4 style="margin-bottom: 5px;">Premium Views</h4>
                    <h2 style="color: #FF5722; margin: 0;">{premium_views} <span style="font-size: 16px;">({premium_percentage:.1f}%)</span></h2>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Views over time chart with enhanced styling
            st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
            st.markdown("<h3>Views Over Time</h3>", unsafe_allow_html=True)
            
            # Group by day
            daily_views = filtered_data.groupby(filtered_data["timestamp"].dt.date).size().reset_index()
            daily_views.columns = ["Date", "Views"]
            
            # Create enhanced line chart
            fig = px.line(
                daily_views, 
                x="Date", 
                y="Views",
                title="Daily Page Views",
                labels={"Date": "Date", "Views": "Number of Views"}
            )
            
            # Customize chart appearance
            fig.update_traces(line=dict(color="#4361EE", width=3))
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                title_font=dict(size=18, color="#212529"),
                font=dict(family="Arial, sans-serif", color="#212529"),
                xaxis=dict(
                    gridcolor='rgba(200,200,200,0.2)',
                    title_font=dict(size=14),
                ),
                yaxis=dict(
                    gridcolor='rgba(200,200,200,0.2)',
                    title_font=dict(size=14),
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Chart comparison in columns
            st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
            st.markdown("<h3>Listing Performance Analysis</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Views by listing type
                st.markdown("<h4>Premium vs. Standard Views</h4>", unsafe_allow_html=True)
                
                # Group by listing type
                type_views = filtered_data.groupby("listing_type").size().reset_index()
                type_views.columns = ["Listing Type", "Views"]
                
                # Create enhanced pie chart
                fig = px.pie(
                    type_views, 
                    values="Views", 
                    names="Listing Type",
                    title="Distribution by Listing Type",
                    color_discrete_sequence=["#4361EE", "#FF5722"]
                )
                
                # Customize chart appearance
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    title_font=dict(size=16, color="#212529"),
                    font=dict(family="Arial, sans-serif", color="#212529"),
                    legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Category performance if available
                st.markdown("<h4>Category Performance</h4>", unsafe_allow_html=True)
                
                # Get categories from listings
                categories = []
                for listing_id in filtered_data["listing_id"].unique():
                    listing = get_listing_by_id(listing_id)
                    if listing is not None and 'category' in listing:
                        categories.append(listing['category'])
                
                if categories:
                    # Count occurrences of each category
                    category_counts = pd.Series(categories).value_counts().reset_index()
                    category_counts.columns = ["Category", "Views"]
                    
                    # Create bar chart
                    fig = px.bar(
                        category_counts.head(5),  # Top 5 categories
                        x="Category", 
                        y="Views",
                        title="Top 5 Categories by Views",
                        color_discrete_sequence=["#4361EE"]
                    )
                    
                    # Customize chart appearance
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        title_font=dict(size=16, color="#212529"),
                        font=dict(family="Arial, sans-serif", color="#212529"),
                        xaxis=dict(
                            gridcolor='rgba(200,200,200,0.2)',
                            title_font=dict(size=14),
                        ),
                        yaxis=dict(
                            gridcolor='rgba(200,200,200,0.2)',
                            title_font=dict(size=14),
                        )
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Category data not available for analysis.")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Top listings table with enhanced styling
            st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
            st.markdown("<h3>Top Performing Listings</h3>", unsafe_allow_html=True)
            st.markdown("<p>Top 10 most viewed business listings in the selected time period</p>", unsafe_allow_html=True)
            
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
            
            # Display enhanced table
            st.dataframe(
                top_listings, 
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Listing Name": st.column_config.TextColumn(
                        "Business Name",
                        width="large",
                    ),
                    "Category": st.column_config.TextColumn(
                        "Category",
                        width="medium",
                    ),
                    "Type": st.column_config.TextColumn(
                        "Listing Type",
                        width="medium",
                    ),
                    "Views": st.column_config.NumberColumn(
                        "Page Views",
                        format="%d",
                        width="small",
                    ),
                    "Listing ID": st.column_config.TextColumn(
                        "ID",
                        width="small",
                    ),
                }
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Daily breakdown with enhanced styling
            st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
            st.markdown("<h3>Daily Breakdown</h3>", unsafe_allow_html=True)
            
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
                st.markdown(f"<h4>Hourly Breakdown for {selected_date}</h4>", unsafe_allow_html=True)
                
                # Group by hour
                hourly_data = date_data.groupby(date_data["timestamp"].dt.hour).size().reset_index()
                hourly_data.columns = ["Hour", "Views"]
                
                # Create enhanced bar chart
                fig = px.bar(
                    hourly_data, 
                    x="Hour", 
                    y="Views",
                    title=f"Views by Hour on {selected_date}",
                    labels={"Hour": "Hour of Day", "Views": "Number of Views"},
                    color_discrete_sequence=["#4361EE"]
                )
                
                # Customize chart appearance
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    title_font=dict(size=16, color="#212529"),
                    font=dict(family="Arial, sans-serif", color="#212529"),
                    xaxis=dict(
                        gridcolor='rgba(200,200,200,0.2)',
                        title_font=dict(size=14),
                    ),
                    yaxis=dict(
                        gridcolor='rgba(200,200,200,0.2)',
                        title_font=dict(size=14),
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Need at least two different dates for daily breakdown analysis.")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Export options with enhanced styling
            st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
            st.markdown("<h3>Export Data</h3>", unsafe_allow_html=True)
            st.markdown("<p>Download analytics data for further analysis</p>", unsafe_allow_html=True)
            
            # Export options in columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<h4>CSV Export</h4>", unsafe_allow_html=True)
                # Convert to CSV
                csv = filtered_data.to_csv(index=False).encode('utf-8')
                
                # Create download button
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"directory_analytics_{start_date}_to_{end_date}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
            with col2:
                st.markdown("<h4>Report Options</h4>", unsafe_allow_html=True)
                report_type = st.selectbox(
                    "Report Type",
                    ["Full Analytics Report", "Listing Performance Only", "Traffic Overview"]
                )
                
                # Placeholder button for PDF generation - would be implemented in a real app
                st.button("Generate PDF Report", key="pdf_report", use_container_width=True, disabled=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

    # Navigation with styled buttons
    st.markdown('<div style="margin-top: 30px; display: flex; justify-content: center;">', unsafe_allow_html=True)
    if st.button("← Return to Admin Dashboard", use_container_width=True):
        st.switch_page("pages/05_Admin_Login.py")
    st.markdown('</div>', unsafe_allow_html=True)
