import streamlit as st
from utils import verify_admin, apply_page_styling
from admin import render_admin_dashboard

# Page configuration
st.set_page_config(
    page_title="Admin Login",
    page_icon="🔒",
    layout="wide"
)

# Apply consistent styling across the app
apply_page_styling()

# Add page-specific styles
st.markdown("""
<style>
    /* Login container styling */
    .login-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 30px;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Admin dashboard styling */
    .admin-section {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("Admin Login")

# Check if already logged in
if 'admin_logged_in' in st.session_state and st.session_state['admin_logged_in']:
    render_admin_dashboard()
    
    # Add logout button
    if st.sidebar.button("Logout"):
        st.session_state['admin_logged_in'] = False
        st.rerun()
else:
    # Create a centered login container
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Login form with styled header
        st.markdown('<h3 style="color: #4361EE; margin-bottom: 20px; text-align: center;">Admin Access</h3>', unsafe_allow_html=True)
        
        # Admin icon
        st.markdown('<div style="text-align: center; margin-bottom: 20px;"><img src="https://cdn-icons-png.flaticon.com/512/1077/1077114.png" width="80"></div>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("<p style='text-align: center;'>Please enter your admin credentials</p>", unsafe_allow_html=True)
            
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
