# -------------------- utils/helpers.py --------------------
import os
import requests
import json
import re
from dotenv import load_dotenv

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
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Hugging Face API request failed: {e}")
