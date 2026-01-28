import streamlit as st
from openai import OpenAI

# --- Streamlit Config ---
st.set_page_config(
    page_title="Hey Buddy 👋",
    layout="centered"
)

st.title("🤍 Siddhartha's AI Friend")
st.write("Talk freely. I'm here to listen, support, and chill with you.")

# --- Load API Key ---
api_key = st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error("❌ OPENAI_API_KEY not found in Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

# --- Language Selector ---
language_mode = st.selectbox(
    "🗣️ Choose how I talk to you",
    ["English", "Tenglish (Telugu + English)", "Hinglish (Hindi + English)"]
)

# --- Handle Language Change ---
if "selected_language" not in st.session_state:
    st.session_state.selected_language = language_mode

if st.session_state.selected_language != language_mode:
    st.session_state.selected_language = language_mode
    st.session_state.messages = []
    st.rerun()

# --- Initialize Chat ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are Siddhartha's AI friend. "
                "You talk like a close, supportive friend, not like a teacher or chatbot. "
                "You listen patiently, respond with empathy, encouragement, and honesty. "
                "You can talk about daily life, stress, motivation, studies, career, "
                "friendships, relationships, self-doubt, fun topics, and random thoughts. "
                "Keep replies natural, warm, and human-like. "
                "If the user is sad or stressed, comfort them first before giving advice. "
                f"Use this language style: {language_mode}. "
                "Never sound robotic or overly formal."
            ),
        }
    ]

# --- Display Messages (Hide system messages) ---
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# --- User Input ---
user_input = st.chat_input("Say anything... I'm listening 🙂")

if user_input:
    # Add user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.write("🤔 Thinking...")

        try:
            # Limit history to avoid token overflow
            st.session_state.messages = st.session_state.messages[-15:]

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

        except Exception:
            placeholder.write("⚠️ Something went wrong. Please try again.")
