import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# =====================
# Gemini setup
# =====================
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


st.title("⚖️ Legal Advising Agent (Gemini)")

if "chat" not in st.session_state:
    st.session_state.chat = []


# =====================
# Chat input
# =====================
user_input = st.chat_input("Ask a legal question...")

if user_input:
    st.session_state.chat.append(("You", user_input))

    prompt = f"""
You are a legal information assistant.
Explain clearly. Do not provide illegal help.

User: {user_input}
"""

    response = model.generate_content(prompt)
    answer = response.text

    answer += "\n\n⚠️ Educational only. Not legal advice."

    st.session_state.chat.append(("Agent", answer))


# =====================
# Show chat
# =====================
for role, msg in st.session_state.chat:
    with st.chat_message(role):
        st.write(msg)
