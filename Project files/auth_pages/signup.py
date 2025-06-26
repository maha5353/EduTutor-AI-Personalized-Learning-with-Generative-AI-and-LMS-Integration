import streamlit as st
from utils.auth import register_user

def signup_page():
    st.subheader("📝 Sign Up")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    usertype = st.selectbox("Choose User Type", ["student", "edututor"])
    
    if st.button("Create Account"):
        if not username or not password:
            st.warning("Username and password cannot be empty.")
        elif register_user(username, password, usertype):
            st.success("✅ User registered! You can now log in.")
        else:
            st.error("❌ Username already exists.")
