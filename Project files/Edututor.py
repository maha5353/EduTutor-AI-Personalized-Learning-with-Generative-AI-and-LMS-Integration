import streamlit as st
from auth_pages.login import login_page
from auth_pages.signup import signup_page

st.set_page_config(page_title="EduTutor", layout="centered")

# Initialize session state defaults
st.session_state.setdefault("is_logged_in", False)
st.session_state.setdefault("username", "")
st.session_state.setdefault("usertype", "")

# Hide sidebar before login
if not st.session_state.is_logged_in:
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Main App UI
st.title("🎓 EduTutor")

if st.session_state.is_logged_in:
    st.success(f"Welcome, {st.session_state.username} ({st.session_state.usertype})!")
    st.markdown("Use the sidebar to access your dashboard and quizzes.")

    if st.button("🔓 Logout"):
        # Clear login-related session state
        st.session_state.is_logged_in = False
        st.session_state.username = ""
        st.session_state.usertype = ""
        st.rerun()  # ✅ Correct method for rerunning the app
else:
    tab = st.radio("Choose an option:", ["🔐 Login", "📝 Sign Up"])
    if tab == "🔐 Login":
        login_page()
    else:
        signup_page()