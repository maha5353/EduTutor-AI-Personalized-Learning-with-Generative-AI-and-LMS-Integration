import streamlit as st
import requests
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()

# Google OAuth2 config
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8501/")

AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

def login_page():
    st.subheader("🔐 Login to EduTutor")

    # --- Username and Password Login ---
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        usertype = st.selectbox("Select your role", ["student", "edututor"])
        login_btn = st.form_submit_button("Login")

    if login_btn:
        if username and password:
            # Simulate login
            st.session_state.is_logged_in = True
            st.session_state.username = username
            st.session_state.usertype = usertype
            st.success(f"✅ Logged in as {usertype.capitalize()}")
            st.rerun()
        else:
            st.error("❌ Please enter both username and password.")

    # --- Divider ---
    st.markdown("---")
    st.markdown("### Or login with Google")

    # Step 1: Generate Google login URL
    auth_params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    auth_url = AUTH_URL + "?" + urllib.parse.urlencode(auth_params)

    # Styled Google button
    # Styled Google Sign-In button
    # Styled Google Sign-In button using a hosted logo
    st.markdown(f"""
    <style>
    .google-btn {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background-color: white;
        color: #444;
        border: 1px solid #ddd;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 600;
        padding: 12px 24px;
        text-decoration: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        margin-top: 1rem;
    }}
    .google-btn:hover {{
        background-color: #f7f7f7;
        border-color: #ccc;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }}
    .google-btn img {{
        height: 22px;
        width: 22px;
        margin-right: 12px;
    }}
    </style>

    <a class="google-btn" href="{auth_url}">
        <img src="https://developers.google.com/identity/images/g-logo.png" alt="Google logo">
        Sign in with Google
    </a>
""", unsafe_allow_html=True)



    # Step 2: Handle redirected code
    if "code" in st.query_params:
        code = st.query_params["code"]

        token_data = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code"
        }

        token_response = requests.post(TOKEN_URL, data=token_data)
        if token_response.status_code == 200:
            tokens = token_response.json()
            access_token = tokens.get("access_token")

            user_info = requests.get(USER_INFO_URL, headers={
                "Authorization": f"Bearer {access_token}"
            }).json()

            st.session_state.is_logged_in = True
            st.session_state.username = user_info.get("name", "Google User")
            st.session_state.usertype = "google"

            st.success(f"✅ Welcome, {st.session_state.username} (Google)!")
            st.rerun()
        else:
            st.error("❌ Google login failed. Try again.")
