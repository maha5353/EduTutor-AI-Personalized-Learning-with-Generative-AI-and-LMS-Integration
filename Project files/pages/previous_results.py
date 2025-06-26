import streamlit as st
import pandas as pd

st.set_page_config(page_title="Previous Results", layout="wide")
st.title("📝 Previous Quiz Results")

if "quiz_history" not in st.session_state or not st.session_state.quiz_history:
    st.info("No previous results available.")
    st.stop()

# Create DataFrame
df = pd.DataFrame(st.session_state.quiz_history)

# Show in table
st.subheader("📊 History Table")
st.dataframe(df, use_container_width=True)

# Optional: download CSV
csv_data = df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download as CSV", csv_data, "quiz_results.csv", "text/csv")
