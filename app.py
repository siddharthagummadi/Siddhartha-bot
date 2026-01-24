import streamlit as st
from openai import OpenAI
import os

# --- Use Streamlit Secrets (secure) ---
api_key = st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("❌ OPENAI_API_KEY not found in Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

# --- Streamlit UI ---
st.set_page_config(page_title="Siddhartha Career Assistant", layout="centered")

st.title("🎓 Siddhartha Placement & Career Assistant")
st.write("Your personalised career assistant for Bhilwara degree students.")

# Initialize chat history with Bhilwara-specific system prompt
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a placement and career assistant for students in Hyderabad. "
                "Guide them for IT jobs, government jobs, internships, resume building, "
                "communication skills, coding basics, interview preparation, "
                "and practical career paths suitable for students from small towns, degree colleges, "
                "and rural backgrounds. Use simple English and optional Tenglish. "
                "Give realistic, actionable advice for Bhilwara students."
            ),
        }
    ]

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Input
user_input = st.chat_input("Ask something about careers, jobs, or placements...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    # Assistant response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.write("Thinking...")

        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=st.session_state.messages
            )

            ai_reply = response.choices[0].message.content
            placeholder.write(ai_reply)

            # Save assistant reply
            st.session_state.messages.append(
                {"role": "assistant", "content": ai_reply}
            )

        except Exception as e:
            placeholder.write(f"Error: {str(e)}")

