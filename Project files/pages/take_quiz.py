import streamlit as st
import os
import requests
import json
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

HF_API_URL = os.getenv("HF_API_URL")
HF_API_KEY = os.getenv("HF_API_KEY")

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

def generate_prompt(topic, difficulty, question_type, num_questions):
    return (
        f"You are a quiz generator AI. Generate {num_questions} {question_type} questions "
        f"on the topic '{topic}' with {difficulty} difficulty.\n"
        "Each question should include options and a correct answer.\n"
        "Format the output strictly as a JSON array like:\n"
        "[{\"question\": ..., \"options\": [...], \"answer\": ..., \"question_type\": ...}, ...]"
    )

def extract_json_array(text):
    """Extract JSON array from raw Hugging Face output."""
    match = re.search(r'(\[\s*{.*?}\s*\])', text, re.DOTALL)
    return match.group(1) if match else None

def query_huggingface(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 1000,
            "temperature": 0.7,
            "return_full_text": False
        }
    }
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        if response.status_code != 200:
            st.error(f"❌ Hugging Face API error: {response.status_code}")
            st.code(response.text)
            return None
        return response.json()
    except Exception as e:
        st.error(f"❌ Request failed: {e}")
        return None

# ---------------- UI ----------------
st.set_page_config(page_title="Edututor AI")
st.title("Edututor AI")

if "quiz" not in st.session_state:
    st.session_state.quiz = []
if "answers" not in st.session_state:
    st.session_state.answers = []
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

# Step 1: Prompt settings
with st.form("quiz_form"):
    topic = st.text_input("Enter Topic", "Machine Learning")
    difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"])
    question_type = st.selectbox("Question Type", ["mcq", "true/false"])
    num_questions = st.slider("Number of Questions", 1, 10, 5)
    generate_btn = st.form_submit_button("🎲 Generate Quiz")

# Step 2: Generate quiz from Hugging Face
if generate_btn:
    prompt = generate_prompt(topic, difficulty, question_type, num_questions)
    with st.spinner("Generating quiz..."):
        response = query_huggingface(prompt)

    if response and isinstance(response, list) and "generated_text" in response[0]:
        raw = response[0]["generated_text"]
        json_data = extract_json_array(raw)
        try:
            quiz = json.loads(json_data)
            st.session_state.quiz = quiz
            st.session_state.answers = [None] * len(quiz)
            st.session_state.quiz_submitted = False
            st.success("✅ Quiz generated successfully!")
        except Exception as e:
            st.error(f"❌ Failed to parse quiz: {e}")
    else:
        st.error("❌ Invalid response from Hugging Face API.")

# Step 3: Take the quiz
if st.session_state.quiz and not st.session_state.quiz_submitted:
    st.markdown("---")
    st.subheader("📝 Your Quiz")

    with st.form("quiz_submission_form"):
        for i, q in enumerate(st.session_state.quiz):
            st.markdown(f"**Q{i+1}: {q.get('question', 'No question')}**")
            q_type = q.get("question_type", "mcq").lower()
            options = q.get("options", [])

            if q_type in ["mcq", "true/false"] and options:
                answer = st.radio("Choose one:", options, key=f"ans_{i}")
            else:
                answer = st.text_input("Your answer:", key=f"ans_{i}_text")
            st.session_state.answers[i] = answer
        submit_btn = st.form_submit_button("✅ Submit Answers")

    if submit_btn:
        st.session_state.quiz_submitted = True

# Step 4: Evaluate and show results
# Step 4: Evaluate and show results
from datetime import datetime

if st.session_state.quiz_submitted:
    st.markdown("---")
    st.subheader("📊 Results")
    score = 0

    for i, q in enumerate(st.session_state.quiz):
        user_ans = st.session_state.answers[i]
        correct_ans = q.get("answer", "").strip().lower()
        user_cleaned = user_ans.strip().lower() if isinstance(user_ans, str) else ""

        is_correct = (user_cleaned == correct_ans)
        if is_correct:
            score += 1

        st.markdown(f"**Q{i+1}: {q['question']}**")
        for opt in q.get("options", []):
            st.markdown(f"- {opt}")
        st.markdown(f"Your answer: `{user_ans}`")
        st.markdown(f"Correct answer: `{correct_ans}`")
        st.markdown("✅ Correct" if is_correct else "❌ Incorrect")
        st.markdown("---")

    st.success(f"🎯 You scored {score} out of {len(st.session_state.quiz)}")

    # ✅ Store the quiz result
    if "quiz_history" not in st.session_state:
        st.session_state.quiz_history = []

    history_entry = {
        "timestamp": datetime.now().isoformat(),
        "topic": topic,
        "difficulty": difficulty,
        "question_type": question_type,
        "score": score,
        "total": len(st.session_state.quiz)
    }

    st.session_state.quiz_history.append(history_entry)

    # Reset for next quiz
    if st.button("🌀 Try Another Quiz"):
        st.session_state.quiz = []
        st.session_state.answers = []
        st.session_state.quiz_submitted = False
