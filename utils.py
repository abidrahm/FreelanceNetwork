import streamlit as st
import pandas as pd
import os
from datetime import datetime
import hashlib
import re

def apply_page_styling():
    """Apply consistent styling to Streamlit pages."""
    st.markdown("""
    <style>
        /* Button styling */
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
        
        /* Card styling */
        .card {
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            background-color: #FFFFFF;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        /* Form styling */
        div.stTextInput > div > div > input {
            border-radius: 4px;
            border: 1px solid #e0e0e0;
            padding: 10px;
        }
        div.stTextInput > div > div > input:focus {
            border-color: #4361EE;
            box-shadow: 0 0 0 0.2rem rgba(67, 97, 238, 0.25);
        }
        
        /* Info box styling */
        div.stAlert > div {
            border-radius: 10px;
            padding: 15px;
        }
    </style>
    """, unsafe_allow_html=True)

def is_valid_url(url):
    """Check if URL is valid."""
    url_pattern = re.compile(
        r'^(http|https)://'  # http:// or https://
        r'([a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?'
        r'(/[a-zA-Z0-9-._~:/?#[\]@!$&\'()*+,;=]*)?$'
    )
    return bool(url_pattern.match(url))

def is_valid_email(email):
    """Check if email is valid."""
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return bool(email_pattern.match(email))

def generate_id():
    """Generate a unique ID based on current timestamp."""
    return hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()[:10]

def verify_admin(username, password):
    """Verify admin credentials."""
    # In a real app, this should be more secure
    # For demonstration purposes, using a simple check
    return username == "admin" and password == "directory_admin"

def track_page_view(listing_id, listing_type="standard"):
    """Track a page view for analytics."""
    analytics_file = "data/analytics.csv"
    
    # Create analytics file if it doesn't exist
    if not os.path.exists(analytics_file):
        analytics_df = pd.DataFrame(columns=["timestamp", "listing_id", "listing_type"])
        analytics_df.to_csv(analytics_file, index=False)
    
    # Load existing analytics
    analytics_df = pd.read_csv(analytics_file)
    
    # Add new page view
    new_view = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "listing_id": listing_id,
        "listing_type": listing_type
    }
    
    analytics_df = pd.concat([analytics_df, pd.DataFrame([new_view])], ignore_index=True)
    analytics_df.to_csv(analytics_file, index=False)

def get_listing_views(listing_id):
    """Get the number of views for a specific listing."""
    analytics_file = "data/analytics.csv"
    
    if not os.path.exists(analytics_file):
        return 0
    
    analytics_df = pd.read_csv(analytics_file)
    return len(analytics_df[analytics_df["listing_id"] == listing_id])
