import streamlit as st
import pandas as pd
from data_manager import add_premium_listing, get_listing_by_id

# Page configuration
st.set_page_config(
    page_title="Premium Options",
    page_icon="⭐",
    layout="wide"
)

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

# Display premium options in cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("## Basic Package")
    st.markdown("### $29")
    st.markdown("**Duration: 30 days**")
    st.markdown("#### Features:")
    st.markdown("- ✅ Higher placement in listings")
    st.markdown("- ✅ Enhanced visibility")
    st.markdown("- ✅ Basic analytics on views")
    
    basic_selected = st.button("Select Basic Package", key="select_basic")

with col2:
    st.markdown("## Standard Package")
    st.markdown("### $49")
    st.markdown("**Duration: 60 days**")
    st.markdown("#### Features:")
    st.markdown("- ✅ Featured on category pages")
    st.markdown("- ✅ 60 days premium visibility")
    st.markdown("- ✅ Enhanced listing details")
    st.markdown("- ✅ Detailed analytics dashboard")
    
    standard_selected = st.button("Select Standard Package", key="select_standard")

with col3:
    st.markdown("## Premium Package")
    st.markdown("### $99")
    st.markdown("**Duration: 90 days**")
    st.markdown("#### Features:")
    st.markdown("- ✅ Featured on homepage")
    st.markdown("- ✅ 90 days premium visibility")
    st.markdown("- ✅ Enhanced listing details")
    st.markdown("- ✅ Featured in search results")
    st.markdown("- ✅ Comprehensive analytics")
    st.markdown("- ✅ Social media promotion")
    
    premium_selected = st.button("Select Premium Package", key="select_premium")

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

# Checkout process
if 'checkout' in st.session_state:
    checkout = st.session_state['checkout']
    
    st.markdown("---")
    st.header("Checkout")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Payment Information")
        
        # In a real application, this would integrate with a payment processor
        # Here we're just collecting the information
        
        with st.form(key="payment_form"):
            st.write(f"Package: {checkout['package_type']} - ${checkout['price']}")
            
            # Payment details
            st.text_input("Cardholder Name", placeholder="John Doe")
            st.text_input("Card Number", placeholder="4242 4242 4242 4242")
            
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Expiration Date", placeholder="MM/YY")
            with col2:
                st.text_input("CVV", placeholder="123", type="password")
            
            st.text_input("Billing Address", placeholder="123 Main St, City, State, ZIP")
            
            agreement = st.checkbox("I agree to the terms of service and recurring billing policy")
            
            submit_payment = st.form_submit_button(f"Pay ${checkout['price']}")
    
    with col2:
        st.subheader("Order Summary")
        st.write(f"**Package:** {checkout['package_type']}")
        st.write(f"**Duration:** {checkout['duration']} days")
        st.write(f"**Price:** ${checkout['price']}")
        st.write("**Renewal:** Automatic (cancel anytime)")
    
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

# Benefits section
st.markdown("---")
st.header("Benefits of Premium Listings")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Increased Visibility")
    st.write("""
    Premium listings receive up to 5x more views than standard listings. 
    Your business will be prominently displayed at the top of category pages 
    and search results, ensuring maximum exposure to potential customers.
    """)
    
    st.subheader("Competitive Advantage")
    st.write("""
    Stand out from competitors by showcasing your business with enhanced 
    details and premium placement. Be the first business potential customers 
    see when browsing our directory.
    """)

with col2:
    st.subheader("Enhanced Credibility")
    st.write("""
    Premium listings signal to customers that your business is established 
    and professional. The premium badge adds credibility and trustworthiness 
    to your listing.
    """)
    
    st.subheader("Detailed Analytics")
    st.write("""
    Gain insights into how customers interact with your listing. 
    Premium packages include detailed analytics on views, clicks, 
    and user engagement, helping you understand your ROI.
    """)

# Testimonials
st.markdown("---")
st.header("Success Stories")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    > "After upgrading to a premium listing, our website traffic increased by 45% in the first month. 
    > The visibility was worth every penny."
    
    **- Sarah J., Owner of Bright Ideas Consulting**
    """)

with col2:
    st.markdown("""
    > "We've gained several new clients directly from our premium directory listing. 
    > The ROI has been incredible for our small business."
    
    **- Michael T., CEO of Tech Solutions Inc.**
    """)

with col3:
    st.markdown("""
    > "The premium placement gave our new restaurant the initial visibility we needed. 
    > We're now booked solid every weekend!"
    
    **- Emma L., Manager at Fresh Bites Eatery**
    """)

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
