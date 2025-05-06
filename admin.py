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
from utils import apply_page_styling

def render_admin_dashboard():
    """Render the admin dashboard."""
    # Apply consistent styling for the admin dashboard
    apply_page_styling()
    
    # Add admin-specific styling
    st.markdown("""
    <style>
        /* Admin dashboard section styling */
        .admin-card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #e0e0e0;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        /* Stats counter styling */
        .stat-counter {
            background-color: #F8F9FA;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #4361EE;
        }
        
        /* Listing table styling */
        .styled-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
            font-size: 14px;
        }
        .styled-table th {
            background-color: #F0F3FF;
            padding: 12px 15px;
            text-align: left;
            border-bottom: 2px solid #4361EE;
        }
        .styled-table td {
            padding: 10px 15px;
            border-bottom: 1px solid #e0e0e0;
        }
        .styled-table tr:nth-child(even) {
            background-color: #F8F9FA;
        }
        .styled-table tr:hover {
            background-color: #F0F3FF;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("Admin Dashboard")
    
    # Admin tabs with enhanced styling
    tab1, tab2, tab3 = st.tabs(["📋 Listing Management", "📊 Analytics", "⚙️ Settings"])
    
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
    
    # Dashboard stats in styled cards
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_listings = len(listings)
        st.markdown(f"""
        <div class="stat-counter">
            <h4 style="margin-bottom: 5px;">Total Listings</h4>
            <h2 style="color: #4361EE; margin: 0;">{total_listings}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        approved_count = len(listings[listings["approved"] == True])
        st.markdown(f"""
        <div class="stat-counter" style="border-left-color: #2EC4B6;">
            <h4 style="margin-bottom: 5px;">Approved</h4>
            <h2 style="color: #2EC4B6; margin: 0;">{approved_count}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        pending_count = len(listings[listings["approved"] == False])
        st.markdown(f"""
        <div class="stat-counter" style="border-left-color: #FF9F1C;">
            <h4 style="margin-bottom: 5px;">Pending</h4>
            <h2 style="color: #FF9F1C; margin: 0;">{pending_count}</h2>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Filter options in a styled card
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.markdown("<h3>Filter Listings</h3>", unsafe_allow_html=True)
    
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
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply filters
    filtered_listings = listings.copy()
    
    if filter_status == "Approved":
        filtered_listings = filtered_listings[filtered_listings["approved"] == True]
    elif filter_status == "Pending":
        filtered_listings = filtered_listings[filtered_listings["approved"] == False]
    
    if filter_category != "All":
        filtered_listings = filtered_listings[filtered_listings["category"] == filter_category]
    
    # Display listings with actions in a styled card
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.markdown("<h3>Manage Listings</h3>", unsafe_allow_html=True)
    st.markdown(f"<p>Showing {len(filtered_listings)} listings</p>", unsafe_allow_html=True)
    
    # Display listings with actions
    for i, row in filtered_listings.iterrows():
        with st.expander(f"{row['name']} - {row['category']} - {'✅ Approved' if row['approved'] else '⏳ Pending'}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div style="padding: 10px; background-color: #F8F9FA; border-radius: 5px; margin-bottom: 10px;">
                    <strong>Description:</strong> {row['description']}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 15px;">
                    <div><strong>Website:</strong> <a href="{row['website']}" target="_blank">{row['website']}</a></div>
                    <div><strong>Contact:</strong> {row['email']} | {row['phone']}</div>
                    <div><strong>Location:</strong> {row['location']}</div>
                    <div><strong>Submitted:</strong> {row['submitted_date']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if not row['approved']:
                    if st.button("Approve", key=f"approve_{row['id']}", use_container_width=True):
                        approve_listing(row['id'])
                        st.success("Listing approved!")
                        st.rerun()
                
                if st.button("Delete", key=f"delete_{row['id']}", use_container_width=True):
                    delete_listing(row['id'])
                    st.success("Listing deleted!")
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_analytics():
    """Render the analytics section."""
    st.header("Analytics Dashboard")
    
    analytics_data = get_analytics_data()
    
    if analytics_data.empty:
        st.info("No analytics data available yet.")
        return
    
    # Convert timestamp to datetime
    analytics_data["timestamp"] = pd.to_datetime(analytics_data["timestamp"])
    
    # Date filter in a styled card
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.markdown("<h3>Filter Data</h3>", unsafe_allow_html=True)
    
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
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Filter by date
    filtered_data = analytics_data[
        (analytics_data["timestamp"].dt.date >= start_date) &
        (analytics_data["timestamp"].dt.date <= end_date)
    ]
    
    if filtered_data.empty:
        st.info("No data available for the selected date range.")
        return
    
    # Overview stats
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.markdown("<h3>Overview</h3>", unsafe_allow_html=True)
    
    # Stats in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_views = len(filtered_data)
        st.markdown(f"""
        <div class="stat-counter">
            <h4 style="margin-bottom: 5px;">Total Views</h4>
            <h2 style="color: #4361EE; margin: 0;">{total_views}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        premium_views = len(filtered_data[filtered_data["listing_type"] == "premium"])
        st.markdown(f"""
        <div class="stat-counter" style="border-left-color: #FF5722;">
            <h4 style="margin-bottom: 5px;">Premium Views</h4>
            <h2 style="color: #FF5722; margin: 0;">{premium_views}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        standard_views = len(filtered_data[filtered_data["listing_type"] == "standard"])
        st.markdown(f"""
        <div class="stat-counter" style="border-left-color: #6c757d;">
            <h4 style="margin-bottom: 5px;">Standard Views</h4>
            <h2 style="color: #6c757d; margin: 0;">{standard_views}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Views over time chart
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.markdown("<h3>Traffic Analysis</h3>", unsafe_allow_html=True)
    
    # Views by day
    daily_views = filtered_data.groupby(filtered_data["timestamp"].dt.date).size().reset_index()
    daily_views.columns = ["Date", "Views"]
    
    # Update chart styling
    fig1 = px.line(
        daily_views, 
        x="Date", 
        y="Views",
        title="Page Views Over Time"
    )
    
    # Customize chart appearance
    fig1.update_traces(line=dict(color="#4361EE", width=3))
    fig1.update_layout(
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
    
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Distribution charts
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.markdown("<h3>Listing Performance</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Views by listing type
        type_views = filtered_data.groupby("listing_type").size().reset_index()
        type_views.columns = ["Listing Type", "Views"]
        
        # Update pie chart styling
        fig2 = px.pie(
            type_views, 
            values="Views", 
            names="Listing Type",
            title="Views by Listing Type",
            color_discrete_sequence=["#4361EE", "#FF5722", "#2EC4B6"]
        )
        
        # Customize chart appearance
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font=dict(size=16, color="#212529"),
            font=dict(family="Arial, sans-serif", color="#212529"),
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        # Top listings
        top_listings = filtered_data.groupby("listing_id").size().reset_index()
        top_listings.columns = ["Listing ID", "Views"]
        top_listings = top_listings.sort_values("Views", ascending=False).head(5)
        
        # Add listing names
        top_listings["Listing Name"] = top_listings["Listing ID"].apply(
            lambda x: get_listing_by_id(x)["name"] if get_listing_by_id(x) is not None else "Unknown"
        )
        
        # Create bar chart for top listings
        fig3 = px.bar(
            top_listings, 
            x="Views", 
            y="Listing Name",
            title="Top 5 Listings by Views", 
            orientation='h',
            color_discrete_sequence=["#4361EE"]
        )
        
        # Customize chart appearance
        fig3.update_layout(
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
        
        st.plotly_chart(fig3, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Detailed data table
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.markdown("<h3>Top Listings by Views</h3>", unsafe_allow_html=True)
    
    # Get top 10 listings
    top_listings = filtered_data.groupby("listing_id").size().reset_index()
    top_listings.columns = ["Listing ID", "Views"]
    top_listings = top_listings.sort_values("Views", ascending=False).head(10)
    
    # Add listing names
    top_listings["Listing Name"] = top_listings["Listing ID"].apply(
        lambda x: get_listing_by_id(x)["name"] if get_listing_by_id(x) is not None else "Unknown"
    )
    
    # Display enhanced table
    st.dataframe(
        top_listings[["Listing Name", "Views", "Listing ID"]], 
        use_container_width=True,
        hide_index=True
    )
    
    # Export options
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "Export to CSV",
            top_listings.to_csv(index=False).encode('utf-8'),
            "listing_analytics.csv",
            "text/csv",
            key='download-csv'
        )
    
    with col2:
        st.button("Generate PDF Report", key="generate_pdf", disabled=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

def render_settings():
    """Render the settings section."""
    st.header("Directory Settings")
    
    # Monetization settings card
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.markdown("<h3>Monetization Settings</h3>", unsafe_allow_html=True)
    st.markdown("<p>Configure premium package pricing and features</p>", unsafe_allow_html=True)
    
    # Premium package settings
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color: #F8F9FA; border-radius: 10px; padding: 15px; height: 100%;">
            <h4 style="color: #4361EE; margin-bottom: 15px;">Basic Package</h4>
        """, unsafe_allow_html=True)
        basic_price = st.number_input("Price ($)", value=29, key="basic_price")
        st.markdown(f"""
            <div style="margin-top: 15px;">
                <p><strong>Price:</strong> ${basic_price}</p>
                <p><strong>Duration:</strong> 30 days</p>
                <p><strong>Features:</strong></p>
                <ul style="padding-left: 20px;">
                    <li>Higher placement in listings</li>
                    <li>Enhanced visibility</li>
                    <li>Basic analytics on views</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #F0F7FF; border-radius: 10px; padding: 15px; height: 100%; position: relative;">
            <div style="position: absolute; top: -10px; right: 10px; background-color: #FF5722; color: white; padding: 3px 10px; border-radius: 20px; font-size: 12px; font-weight: bold;">POPULAR</div>
            <h4 style="color: #4361EE; margin-bottom: 15px;">Standard Package</h4>
        """, unsafe_allow_html=True)
        standard_price = st.number_input("Price ($)", value=49, key="standard_price")
        st.markdown(f"""
            <div style="margin-top: 15px;">
                <p><strong>Price:</strong> ${standard_price}</p>
                <p><strong>Duration:</strong> 60 days</p>
                <p><strong>Features:</strong></p>
                <ul style="padding-left: 20px;">
                    <li>Featured on category pages</li>
                    <li>60 days premium visibility</li>
                    <li>Enhanced listing details</li>
                    <li>Detailed analytics dashboard</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: #F0F3FF; border: 1px solid #4361EE; border-radius: 10px; padding: 15px; height: 100%;">
            <h4 style="color: #4361EE; margin-bottom: 15px;">Premium Package</h4>
        """, unsafe_allow_html=True)
        premium_price = st.number_input("Price ($)", value=99, key="premium_price")
        st.markdown(f"""
            <div style="margin-top: 15px;">
                <p><strong>Price:</strong> ${premium_price}</p>
                <p><strong>Duration:</strong> 90 days</p>
                <p><strong>Features:</strong></p>
                <ul style="padding-left: 20px;">
                    <li>Featured on homepage</li>
                    <li>90 days premium visibility</li>
                    <li>Enhanced listing details</li>
                    <li>Featured in search results</li>
                    <li>Comprehensive analytics</li>
                    <li>Social media promotion</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Save settings button with better styling
    st.markdown("<div style='margin-top: 20px;'>", unsafe_allow_html=True)
    if st.button("Save Pricing Settings", use_container_width=True):
        st.success("Settings saved successfully!")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # General settings card
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.markdown("<h3>General Settings</h3>", unsafe_allow_html=True)
    
    # Two-column layout for settings
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h4>Directory Configuration</h4>", unsafe_allow_html=True)
        st.toggle("Require approval for new listings", value=True, key="require_approval")
        st.toggle("Allow public submissions", value=True, key="allow_submissions")
        st.toggle("Show premium labels", value=True, key="show_premium_labels")
        st.toggle("Enable analytics tracking", value=True, key="enable_analytics")
        st.number_input("Maximum listings per page", value=12, key="max_listings_per_page")
    
    with col2:
        st.markdown("<h4>Email Notifications</h4>", unsafe_allow_html=True)
        st.toggle("New listing submitted", value=True, key="email_new_listing")
        st.toggle("Premium purchase", value=True, key="email_premium_purchase")
        st.toggle("Send weekly reports", value=False, key="email_weekly_reports")
        st.text_input("Admin email address", value="admin@example.com", key="admin_email")
    
    # Save settings button
    if st.button("Save General Settings", use_container_width=True):
        st.success("General settings saved successfully!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Appearance settings
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.markdown("<h3>Appearance Settings</h3>", unsafe_allow_html=True)
    st.markdown("<p>Customize the look and feel of your directory</p>", unsafe_allow_html=True)
    
    # Sample color palette
    st.markdown("""
    <div style="display: flex; margin-bottom: 20px; gap: 10px;">
        <div style="background-color: #4361EE; width: 50px; height: 50px; border-radius: 5px;"></div>
        <div style="background-color: #FF5722; width: 50px; height: 50px; border-radius: 5px;"></div>
        <div style="background-color: #2EC4B6; width: 50px; height: 50px; border-radius: 5px;"></div>
        <div style="background-color: #FF9F1C; width: 50px; height: 50px; border-radius: 5px;"></div>
        <div style="background-color: #212529; width: 50px; height: 50px; border-radius: 5px;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.color_picker("Primary Color", "#4361EE", key="primary_color")
        st.color_picker("Secondary Color", "#FF5722", key="secondary_color")
        st.selectbox("Font Family", ["Arial, sans-serif", "Roboto, sans-serif", "Open Sans, sans-serif"], key="font_family")
    
    with col2:
        st.selectbox("Card Style", ["Rounded corners", "Sharp corners", "Elevated"], key="card_style")
        st.selectbox("Button Style", ["Rounded", "Pill", "Square"], key="button_style")
        st.toggle("Dark Mode", value=False, key="dark_mode")
    
    # Save appearance button
    if st.button("Save Appearance Settings", use_container_width=True):
        st.success("Appearance settings saved successfully!")
    
    st.markdown('</div>', unsafe_allow_html=True)
