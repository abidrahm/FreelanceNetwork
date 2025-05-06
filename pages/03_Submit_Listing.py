import streamlit as st
import pandas as pd
from data_manager import add_listing, get_categories
from utils import is_valid_url, is_valid_email

# Page configuration
st.set_page_config(
    page_title="Submit Listing",
    page_icon="📝",
    layout="wide"
)

# Title and description
st.title("Submit Your Business Listing")
st.write("Get your business listed in our directory")

# Sidebar with benefits
st.sidebar.title("Benefits of Listing")
st.sidebar.write("Listing your business in our directory provides:")
st.sidebar.markdown("- **Increased Visibility** to potential customers")
st.sidebar.markdown("- **Improved Online Presence** with backlinks to your website")
st.sidebar.markdown("- **Business Credibility** through association with our directory")
st.sidebar.markdown("- **24/7 Exposure** for your services and products")

# Get categories for dropdown
categories = get_categories()
category_options = categories['name'].tolist()

# Submission form
with st.form(key="listing_submission_form"):
    st.subheader("Business Information")
    
    # Basic info
    name = st.text_input("Business Name*", placeholder="Example: Joe's Coffee Shop")
    
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("Business Category*", category_options)
    with col2:
        location = st.text_input("Business Location*", placeholder="City, State/Province, Country")
    
    description = st.text_area(
        "Business Description*", 
        placeholder="Describe your business, services, and unique value proposition (100-500 characters)",
        max_chars=500,
        height=150
    )
    
    st.subheader("Contact Information")
    
    website = st.text_input("Website URL*", placeholder="https://example.com")
    
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Business Email*", placeholder="contact@example.com")
    with col2:
        phone = st.text_input("Business Phone", placeholder="+1 234 567 8900")
    
    # Terms and conditions
    terms_agreement = st.checkbox("I agree to the terms and conditions of listing")
    
    # Submit button
    submit_button = st.form_submit_button("Submit Listing", use_container_width=True)

# Process form submission
if submit_button:
    # Validate required fields
    if not name or not description or not category or not website or not email or not location:
        st.error("Please fill out all required fields (marked with *).")
    elif not is_valid_url(website):
        st.error("Please enter a valid website URL (must include http:// or https://).")
    elif not is_valid_email(email):
        st.error("Please enter a valid email address.")
    elif not terms_agreement:
        st.error("You must agree to the terms and conditions to submit a listing.")
    else:
        # Add the listing
        listing_id = add_listing(
            name=name,
            description=description,
            category=category,
            website=website,
            email=email,
            phone=phone if phone else "Not provided",
            location=location
        )
        
        # Show success message
        st.success("Your listing has been submitted successfully! It will be reviewed by our team before it appears in the directory.")
        
        # Clear form (by resetting session state)
        for key in st.session_state.keys():
            if key.startswith("listing_submission_form"):
                del st.session_state[key]
        
        # Offer premium options
        st.subheader("Enhance Your Listing Visibility")
        st.write("Consider premium placement options to get more visibility for your business.")
        
        if st.button("Explore Premium Options"):
            st.session_state['new_listing_id'] = listing_id
            st.switch_page("pages/04_Premium_Options.py")

# Premium options preview
st.markdown("---")
st.subheader("Premium Placement Options")

# Show premium options
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Basic")
    st.markdown("$29 / month")
    st.markdown("- Higher placement in listings")
    st.markdown("- 30 days premium visibility")

with col2:
    st.markdown("### Standard")
    st.markdown("$49 / month")
    st.markdown("- Featured on category pages")
    st.markdown("- 60 days premium visibility")
    st.markdown("- Enhanced listing details")

with col3:
    st.markdown("### Premium")
    st.markdown("$99 / month")
    st.markdown("- Featured on homepage")
    st.markdown("- 90 days premium visibility")
    st.markdown("- Enhanced listing details")
    st.markdown("- Featured in search results")

# Terms and conditions in expander
with st.expander("Terms and Conditions"):
    st.write("""
    ## Terms and Conditions for Business Directory Listings

    By submitting a listing to our Business Directory, you agree to the following terms and conditions:

    1. **Accuracy of Information**: All information provided must be accurate and truthful. You are responsible for keeping your listing information up to date.

    2. **Appropriate Content**: Listings must not contain offensive, illegal, or inappropriate content. We reserve the right to remove any listing that violates this policy.

    3. **Review Process**: All listings are subject to review before being published. We reserve the right to reject any listing that does not meet our standards.

    4. **Modifications**: We may modify or edit listing content for clarity, grammar, or formatting purposes.

    5. **Removal**: We reserve the right to remove any listing at any time for any reason.

    6. **No Guarantee**: Inclusion in the directory does not guarantee increased business or visibility. Results may vary.

    7. **Data Usage**: Information provided in your listing may be used for analytical purposes and to improve our services.

    8. **Contact Communication**: By providing your contact information, you agree to receive communications from us regarding your listing.

    Last updated: 2023
    """)
