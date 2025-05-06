import streamlit as st
from utils import verify_admin
from admin import render_admin_dashboard

# Page configuration
st.set_page_config(
    page_title="Admin Login",
    page_icon="🔒",
    layout="wide"
)

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
    # Login form
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
    
    # Help text
    st.info("For demonstration, use username 'admin' and password 'directory_admin'")
    
    # Return to main site
    if st.button("Return to Main Site"):
        st.switch_page("app.py")
