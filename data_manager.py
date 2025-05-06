import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# Data file paths
CATEGORIES_FILE = "data/categories.csv"
LISTINGS_FILE = "data/listings.csv"
PREMIUM_LISTINGS_FILE = "data/premium_listings.csv"
ANALYTICS_FILE = "data/analytics.csv"

def initialize_data():
    """Initialize data files if they don't exist."""
    # Create data directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Initialize categories
    if not os.path.exists(CATEGORIES_FILE):
        categories = pd.DataFrame({
            "id": ["cat1", "cat2", "cat3", "cat4", "cat5", "cat6", "cat7", "cat8"],
            "name": [
                "Restaurants", 
                "Retail", 
                "Professional Services", 
                "Health & Wellness", 
                "Technology", 
                "Home Services", 
                "Education", 
                "Entertainment"
            ]
        })
        categories.to_csv(CATEGORIES_FILE, index=False)
    
    # Initialize listings
    if not os.path.exists(LISTINGS_FILE):
        listings = pd.DataFrame(columns=[
            "id", "name", "description", "category", "website", 
            "email", "phone", "location", "submitted_date", "approved"
        ])
        listings.to_csv(LISTINGS_FILE, index=False)
    
    # Initialize premium listings
    if not os.path.exists(PREMIUM_LISTINGS_FILE):
        premium = pd.DataFrame(columns=[
            "id", "listing_id", "package_type", "start_date", "end_date", "payment_status"
        ])
        premium.to_csv(PREMIUM_LISTINGS_FILE, index=False)
    
    # Initialize analytics
    if not os.path.exists(ANALYTICS_FILE):
        analytics = pd.DataFrame(columns=["timestamp", "listing_id", "listing_type"])
        analytics.to_csv(ANALYTICS_FILE, index=False)

def get_categories():
    """Get all categories."""
    if os.path.exists(CATEGORIES_FILE):
        return pd.read_csv(CATEGORIES_FILE)
    return pd.DataFrame(columns=["id", "name"])

def get_all_listings(approved_only=True):
    """Get all listings."""
    if os.path.exists(LISTINGS_FILE):
        listings = pd.read_csv(LISTINGS_FILE)
        if approved_only:
            return listings[listings["approved"] == True]
        return listings
    return pd.DataFrame()

def get_listings_by_category(category, approved_only=True):
    """Get listings by category."""
    listings = get_all_listings(approved_only)
    if not listings.empty:
        return listings[listings["category"] == category]
    return pd.DataFrame()

def get_listing_by_id(listing_id):
    """Get a specific listing by ID."""
    listings = get_all_listings(approved_only=False)
    if not listings.empty:
        listing = listings[listings["id"] == listing_id]
        if not listing.empty:
            return listing.iloc[0]
    return None

def search_listings(query, approved_only=True):
    """Search listings by query."""
    listings = get_all_listings(approved_only)
    if listings.empty:
        return pd.DataFrame()
    
    # Convert query and DataFrame text columns to lowercase for case-insensitive search
    query = query.lower()
    listings_lower = listings.copy()
    for col in ["name", "description", "category", "location"]:
        listings_lower[col] = listings_lower[col].str.lower()
    
    # Search in multiple columns
    mask = (
        listings_lower["name"].str.contains(query, na=False) |
        listings_lower["description"].str.contains(query, na=False) |
        listings_lower["category"].str.contains(query, na=False) |
        listings_lower["location"].str.contains(query, na=False)
    )
    
    return listings[mask]

def add_listing(name, description, category, website, email, phone, location):
    """Add a new listing."""
    listing_id = generate_id()
    new_listing = {
        "id": listing_id,
        "name": name,
        "description": description,
        "category": category,
        "website": website,
        "email": email,
        "phone": phone,
        "location": location,
        "submitted_date": datetime.now().strftime("%Y-%m-%d"),
        "approved": False
    }
    
    if os.path.exists(LISTINGS_FILE):
        listings = pd.read_csv(LISTINGS_FILE)
        listings = pd.concat([listings, pd.DataFrame([new_listing])], ignore_index=True)
        listings.to_csv(LISTINGS_FILE, index=False)
    else:
        pd.DataFrame([new_listing]).to_csv(LISTINGS_FILE, index=False)
    
    return listing_id

def approve_listing(listing_id):
    """Approve a listing."""
    if os.path.exists(LISTINGS_FILE):
        listings = pd.read_csv(LISTINGS_FILE)
        listings.loc[listings["id"] == listing_id, "approved"] = True
        listings.to_csv(LISTINGS_FILE, index=False)
        return True
    return False

def delete_listing(listing_id):
    """Delete a listing."""
    if os.path.exists(LISTINGS_FILE):
        listings = pd.read_csv(LISTINGS_FILE)
        listings = listings[listings["id"] != listing_id]
        listings.to_csv(LISTINGS_FILE, index=False)
        
        # Also remove any premium listings
        if os.path.exists(PREMIUM_LISTINGS_FILE):
            premium = pd.read_csv(PREMIUM_LISTINGS_FILE)
            premium = premium[premium["listing_id"] != listing_id]
            premium.to_csv(PREMIUM_LISTINGS_FILE, index=False)
        return True
    return False

def add_premium_listing(listing_id, package_type, duration_days):
    """Add a premium listing."""
    premium_id = generate_id()
    start_date = datetime.now()
    end_date = start_date + timedelta(days=duration_days)
    
    new_premium = {
        "id": premium_id,
        "listing_id": listing_id,
        "package_type": package_type,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "payment_status": "paid"
    }
    
    if os.path.exists(PREMIUM_LISTINGS_FILE):
        premium = pd.read_csv(PREMIUM_LISTINGS_FILE)
        premium = pd.concat([premium, pd.DataFrame([new_premium])], ignore_index=True)
        premium.to_csv(PREMIUM_LISTINGS_FILE, index=False)
    else:
        pd.DataFrame([new_premium]).to_csv(PREMIUM_LISTINGS_FILE, index=False)
    
    return premium_id

def get_premium_listings():
    """Get all active premium listings."""
    if os.path.exists(PREMIUM_LISTINGS_FILE) and os.path.exists(LISTINGS_FILE):
        premium = pd.read_csv(PREMIUM_LISTINGS_FILE)
        listings = pd.read_csv(LISTINGS_FILE)
        
        # Filter for active premium listings
        today = datetime.now().strftime("%Y-%m-%d")
        active_premium = premium[
            (premium["end_date"] >= today) & 
            (premium["payment_status"] == "paid")
        ]
        
        if active_premium.empty:
            return pd.DataFrame()
        
        # Get full listing details for premium listings
        premium_listing_ids = active_premium["listing_id"].unique()
        premium_listings = listings[
            (listings["id"].isin(premium_listing_ids)) & 
            (listings["approved"] == True)
        ]
        
        return premium_listings
    
    return pd.DataFrame()

def get_analytics_data():
    """Get analytics data."""
    if os.path.exists(ANALYTICS_FILE):
        return pd.read_csv(ANALYTICS_FILE)
    return pd.DataFrame()

def generate_id():
    """Generate a unique ID."""
    return datetime.now().strftime("%Y%m%d%H%M%S") + str(int(datetime.now().microsecond / 1000))
