# pages/1_Dashboard.py

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("📘 Dashboard")

# ------------------ User Info ------------------
username = st.session_state.get("username", "Guest")
usertype = st.session_state.get("usertype", "Student")


st.subheader("👤 User Information")
st.markdown(f"- **Name**: {username}")
st.markdown(f"- **Usertype**: {usertype}")


# ------------------ Quiz Summary ------------------
quiz_history = st.session_state.get("quiz_history", [])

st.subheader("📊 Quiz Summary")

if not quiz_history:
    st.info("You haven't taken any quizzes yet.")
else:
    df = pd.DataFrame(quiz_history)

    total_quizzes = len(df)
    total_score = df["score"].sum()
    total_possible = df["total"].sum()
    avg_score = (total_score / total_possible) * 100 if total_possible > 0 else 0

    st.metric("📝 Total Quizzes Taken", total_quizzes)
    st.metric("🏅 Total Marks Scored", f"{total_score} / {total_possible}")
    st.metric("📈 Average Score", f"{avg_score:.2f} %")
