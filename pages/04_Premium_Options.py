import streamlit as st
import pandas as pd
from data_manager import add_premium_listing, get_listing_by_id

# Page configuration
st.set_page_config(
    page_title="Premium Options",
    page_icon="⭐",
    layout="wide"
)

# Custom CSS to enhance styling
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
    
    /* Package card styling */
    .package-card {
        border-radius: 10px;
        padding: 25px;
        height: 100%;
        transition: transform 0.3s, box-shadow 0.3s;
        position: relative;
    }
    .package-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .package-card.basic {
        background-color: #F8F9FA;
        border: 1px solid #e0e0e0;
    }
    .package-card.standard {
        background-color: #F0F7FF;
        border: 1px solid #B6D0E2;
    }
    .package-card.premium {
        background-color: #F0F3FF;
        border: 1px solid #4361EE;
    }
    .price-tag {
        font-size: 32px;
        font-weight: bold;
        margin: 15px 0;
        color: #4361EE;
    }
    .feature-list {
        margin: 20px 0;
        padding-left: 20px;
    }
    .feature-list li {
        margin-bottom: 8px;
    }
    .popular-badge {
        position: absolute;
        top: -10px;
        right: 20px;
        background-color: #FF5722;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
    }
    
    /* Testimonial card styling */
    .testimonial-card {
        background-color: #fff;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .testimonial-quote {
        font-style: italic;
        color: #495057;
        font-size: 16px;
    }
    .testimonial-author {
        color: #212529;
        font-weight: bold;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("Premium Listing Options")
st.write("Boost your visibility with premium placement")

# Check if we have a new listing to feature
new_listing = None
if 'new_listing_id' in st.session_state:
    new_listing_id = st.session_state['new_listing_id']
    new_listing = get_listing_by_id(new_listing_id)
    
    if new_listing is not None:
        st.success(f"Your listing '{new_listing['name']}' has been submitted! Enhance its visibility with premium options.")

# Premium package information
st.header("Choose Your Premium Package")

# Display premium options in modern styled cards
col1, col2, col3 = st.columns(3)

with col1:
    # Basic package with custom styling
    st.markdown("""
    <div class="package-card basic">
        <h2>Basic Package</h2>
        <div class="price-tag">$29</div>
        <p><strong>Duration: 30 days</strong></p>
        <hr>
        <h4>Features:</h4>
        <ul class="feature-list">
            <li>Higher placement in listings</li>
            <li>Enhanced visibility</li>
            <li>Basic analytics on views</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    basic_selected = st.button("Select Basic Package", key="select_basic", use_container_width=True)

with col2:
    # Standard package with custom styling and popular badge
    st.markdown("""
    <div class="package-card standard">
        <div class="popular-badge">POPULAR</div>
        <h2>Standard Package</h2>
        <div class="price-tag">$49</div>
        <p><strong>Duration: 60 days</strong></p>
        <hr>
        <h4>Features:</h4>
        <ul class="feature-list">
            <li>Featured on category pages</li>
            <li>60 days premium visibility</li>
            <li>Enhanced listing details</li>
            <li>Detailed analytics dashboard</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    standard_selected = st.button("Select Standard Package", key="select_standard", use_container_width=True)

with col3:
    # Premium package with custom styling
    st.markdown("""
    <div class="package-card premium">
        <h2>Premium Package</h2>
        <div class="price-tag">$99</div>
        <p><strong>Duration: 90 days</strong></p>
        <hr>
        <h4>Features:</h4>
        <ul class="feature-list">
            <li>Featured on homepage</li>
            <li>90 days premium visibility</li>
            <li>Enhanced listing details</li>
            <li>Featured in search results</li>
            <li>Comprehensive analytics</li>
            <li>Social media promotion</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    premium_selected = st.button("Select Premium Package", key="select_premium", use_container_width=True)

# Handle package selection
if basic_selected or standard_selected or premium_selected:
    if 'new_listing_id' in st.session_state:
        listing_id = st.session_state['new_listing_id']
        
        # Determine package type and duration
        if basic_selected:
            package_type = "Basic"
            duration = 30
            price = 29
        elif standard_selected:
            package_type = "Standard"
            duration = 60
            price = 49
        else:  # premium_selected
            package_type = "Premium"
            duration = 90
            price = 99
        
        # Show checkout form
        st.session_state['checkout'] = {
            'listing_id': listing_id,
            'package_type': package_type,
            'duration': duration,
            'price': price
        }
        
        st.rerun()
    else:
        st.error("Please submit a listing first before selecting a premium package.")
        if st.button("Submit a Listing"):
            st.switch_page("pages/03_Submit_Listing.py")

# Checkout process with enhanced styling
if 'checkout' in st.session_state:
    checkout = st.session_state['checkout']
    
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>Complete Your Purchase</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Payment form with enhanced styling
        st.markdown("""
        <div style="background-color: white; border: 1px solid #e0e0e0; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
            <h3 style="color: #4361EE; margin-bottom: 20px;">Payment Information</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # In a real application, this would integrate with a payment processor
        with st.form(key="payment_form"):
            st.markdown(f"""
            <div style="background-color: #F8F9FA; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
                <strong>Selected Package:</strong> {checkout['package_type']} - ${checkout['price']}
            </div>
            """, unsafe_allow_html=True)
            
            # Payment details
            st.text_input("Cardholder Name", placeholder="John Doe")
            st.text_input("Card Number", placeholder="4242 4242 4242 4242")
            
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Expiration Date", placeholder="MM/YY")
            with col2:
                st.text_input("CVV", placeholder="123", type="password")
            
            st.text_input("Billing Address", placeholder="123 Main St, City, State, ZIP")
            
            # Styled checkbox for terms
            agreement = st.checkbox("I agree to the terms of service and recurring billing policy")
            
            # Styled submit button (Streamlit will automatically style this with our custom CSS)
            submit_payment = st.form_submit_button(f"Complete Purchase - ${checkout['price']}")
    
    with col2:
        # Order summary with styled card
        st.markdown("""
        <div style="background-color: #F0F3FF; border: 1px solid #4361EE; border-radius: 10px; padding: 20px;">
            <h3 style="color: #212529; margin-bottom: 20px;">Order Summary</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Package details with better styling
        st.markdown(f"""
        <div style="background-color: white; border: 1px solid #e0e0e0; border-radius: 10px; padding: 20px; margin-top: 20px;">
            <p><strong>Package:</strong> {checkout['package_type']}</p>
            <p><strong>Duration:</strong> {checkout['duration']} days</p>
            <p><strong>Price:</strong> ${checkout['price']}</p>
            <p><strong>Renewal:</strong> Automatic (cancel anytime)</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Security note
        st.markdown("""
        <div style="margin-top: 20px; text-align: center;">
            <img src="https://cdn-icons-png.flaticon.com/512/1253/1253776.png" width="30" style="margin-bottom: 10px;">
            <p style="font-size: 14px; color: #6c757d;">Secure payment processing.<br>Your data is encrypted and secure.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Process payment submission
    if submit_payment:
        if not agreement:
            st.error("You must agree to the terms to complete your purchase.")
        else:
            # In a real app, this would process the payment
            # For now, we'll just add the premium listing
            premium_id = add_premium_listing(
                listing_id=checkout['listing_id'],
                package_type=checkout['package_type'],
                duration_days=checkout['duration']
            )
            
            st.success("Payment successful! Your listing has been upgraded to premium status.")
            
            # Clear checkout from session state
            del st.session_state['checkout']
            if 'new_listing_id' in st.session_state:
                del st.session_state['new_listing_id']
            
            if st.button("Return to Home"):
                st.switch_page("app.py")

# Benefits section with modern styling
st.markdown("---")
st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>Benefits of Premium Listings</h2>", unsafe_allow_html=True)

# Use icons and cards for benefits
benefits_data = [
    {
        "icon": "👁️", 
        "title": "Increased Visibility",
        "description": "Premium listings receive up to 5x more views than standard listings. Your business will be prominently displayed at the top of category pages and search results."
    },
    {
        "icon": "🏆", 
        "title": "Competitive Advantage",
        "description": "Stand out from competitors by showcasing your business with enhanced details and premium placement. Be the first business potential customers see."
    },
    {
        "icon": "✅", 
        "title": "Enhanced Credibility",
        "description": "Premium listings signal to customers that your business is established and professional. The premium badge adds credibility and trustworthiness."
    },
    {
        "icon": "📊", 
        "title": "Detailed Analytics",
        "description": "Gain insights into how customers interact with your listing. Track views, clicks, and user engagement to understand your ROI."
    }
]

# Create a 2x2 grid of benefits
col1, col2 = st.columns(2)
cols = [col1, col2]

for i, benefit in enumerate(benefits_data):
    with cols[i % 2]:
        st.markdown(f"""
        <div style="background-color: white; border: 1px solid #e0e0e0; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
            <div style="font-size: 36px; margin-bottom: 10px; text-align: center;">{benefit['icon']}</div>
            <h3 style="color: #4361EE; margin-bottom: 10px; text-align: center;">{benefit['title']}</h3>
            <p>{benefit['description']}</p>
        </div>
        """, unsafe_allow_html=True)

# Testimonials with modern styling
st.markdown("---")
st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>Success Stories</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="testimonial-card">
        <div class="testimonial-quote">
            "After upgrading to a premium listing, our website traffic increased by 45% in the first month. 
            The visibility was worth every penny."
        </div>
        <div class="testimonial-author">
            - Sarah J., Owner of Bright Ideas Consulting
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="testimonial-card">
        <div class="testimonial-quote">
            "We've gained several new clients directly from our premium directory listing. 
            The ROI has been incredible for our small business."
        </div>
        <div class="testimonial-author">
            - Michael T., CEO of Tech Solutions Inc.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="testimonial-card">
        <div class="testimonial-quote">
            "The premium placement gave our new restaurant the initial visibility we needed. 
            We're now booked solid every weekend!"
        </div>
        <div class="testimonial-author">
            - Emma L., Manager at Fresh Bites Eatery
        </div>
    </div>
    """, unsafe_allow_html=True)

# FAQ at the bottom
with st.expander("Frequently Asked Questions"):
    st.markdown("""
    ### How long does it take for my premium listing to appear?
    Premium listings are activated immediately after payment processing, which typically takes 1-2 minutes.
    
    ### Can I upgrade or downgrade my package later?
    Yes, you can change your premium package at any time. The new package will take effect after your current subscription period.
    
    ### Is there a refund policy?
    We offer a 7-day money-back guarantee if you're not satisfied with your premium listing.
    
    ### Will my premium listing auto-renew?
    Yes, premium listings are set to auto-renew by default to ensure uninterrupted premium placement. You can cancel auto-renewal at any time.
    
    ### How do I track the performance of my premium listing?
    Premium listings include an analytics dashboard where you can track views, clicks, and engagement with your listing.
    
    ### Can I have multiple premium listings?
    Yes, you can have multiple premium listings if you have multiple businesses or locations.
    """)
