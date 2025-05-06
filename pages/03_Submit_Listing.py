import streamlit as st
import pandas as pd
from data_manager import add_listing, get_categories
from utils import is_valid_url, is_valid_email, apply_page_styling

# Page configuration
st.set_page_config(
    page_title="Submit Listing",
    page_icon="📝",
    layout="wide"
)

# Apply consistent styling across the app
apply_page_styling()

# Add page-specific styles
st.markdown("""
<style>
    /* Form styling */
    .form-container {
        background-color: white;
        padding: 30px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Benefits card styling */
    .benefits-card {
        background-color: #F0F3FF;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #4361EE;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("Submit Your Business Listing")
st.write("Get your business listed in our directory")

# Sidebar with benefits using enhanced styling
st.sidebar.title("Benefits of Listing")
st.sidebar.markdown('<div class="benefits-card">', unsafe_allow_html=True)
st.sidebar.write("Listing your business in our directory provides:")
st.sidebar.markdown("- **Increased Visibility** to potential customers")
st.sidebar.markdown("- **Improved Online Presence** with backlinks to your website")
st.sidebar.markdown("- **Business Credibility** through association with our directory")
st.sidebar.markdown("- **24/7 Exposure** for your services and products")
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Add a testimonial in the sidebar
st.sidebar.markdown('<div class="benefits-card" style="background-color: #F8F9FA; border-left-color: #6c757d;">', unsafe_allow_html=True)
st.sidebar.markdown("### What our customers say")
st.sidebar.markdown("> *\"Since listing our business in this directory, we've seen a 30% increase in online inquiries. The premium placement was definitely worth the investment!\"*")
st.sidebar.markdown("**— Sarah Johnson, Owner of Bright Designs**")
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Get categories for dropdown
categories = get_categories()
category_options = categories['name'].tolist()

# Submission form with enhanced styling
st.markdown('<div class="form-container">', unsafe_allow_html=True)
with st.form(key="listing_submission_form"):
    st.markdown("<h3 style='color: #4361EE;'>Business Information</h3>", unsafe_allow_html=True)
    
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
    
    st.markdown("<h3 style='color: #4361EE; margin-top: 20px;'>Contact Information</h3>", unsafe_allow_html=True)
    
    website = st.text_input("Website URL*", placeholder="https://example.com")
    
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Business Email*", placeholder="contact@example.com")
    with col2:
        phone = st.text_input("Business Phone", placeholder="+1 234 567 8900")
    
    # Terms and conditions with better styling
    st.markdown("<div style='margin-top: 20px; margin-bottom: 10px;'>", unsafe_allow_html=True)
    terms_agreement = st.checkbox("I agree to the terms and conditions of listing")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Submit button
    submit_button = st.form_submit_button("Submit Listing", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

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

# Premium options preview with enhanced styling
st.markdown("---")
st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>Premium Placement Options</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-bottom: 30px;'>Boost your visibility and stand out from the competition</p>", unsafe_allow_html=True)

# Show premium options with modern cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background-color: #F8F9FA; border: 1px solid #e0e0e0; border-radius: 10px; padding: 20px; height: 100%;">
        <h3 style="color: #4361EE;">Basic</h3>
        <div style="font-size: 28px; font-weight: bold; margin: 15px 0; color: #4361EE;">$29</div>
        <p><strong>Duration: 30 days</strong></p>
        <hr>
        <ul style="margin-top: 15px; padding-left: 20px;">
            <li>Higher placement in listings</li>
            <li>Enhanced visibility</li>
            <li>Basic analytics on views</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background-color: #F0F7FF; border: 1px solid #B6D0E2; border-radius: 10px; padding: 20px; height: 100%; position: relative;">
        <div style="position: absolute; top: -10px; right: 20px; background-color: #FF5722; color: white; padding: 5px 15px; border-radius: 20px; font-size: 14px; font-weight: bold;">POPULAR</div>
        <h3 style="color: #4361EE;">Standard</h3>
        <div style="font-size: 28px; font-weight: bold; margin: 15px 0; color: #4361EE;">$49</div>
        <p><strong>Duration: 60 days</strong></p>
        <hr>
        <ul style="margin-top: 15px; padding-left: 20px;">
            <li>Featured on category pages</li>
            <li>60 days premium visibility</li>
            <li>Enhanced listing details</li>
            <li>Detailed analytics dashboard</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background-color: #F0F3FF; border: 1px solid #4361EE; border-radius: 10px; padding: 20px; height: 100%;">
        <h3 style="color: #4361EE;">Premium</h3>
        <div style="font-size: 28px; font-weight: bold; margin: 15px 0; color: #4361EE;">$99</div>
        <p><strong>Duration: 90 days</strong></p>
        <hr>
        <ul style="margin-top: 15px; padding-left: 20px;">
            <li>Featured on homepage</li>
            <li>90 days premium visibility</li>
            <li>Enhanced listing details</li>
            <li>Featured in search results</li>
            <li>Comprehensive analytics</li>
            <li>Social media promotion</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

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
