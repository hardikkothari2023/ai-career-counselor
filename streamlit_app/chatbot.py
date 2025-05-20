import os
import requests
import streamlit as st

# ✅ Load OpenRouter API key from secrets or environment variable
openrouter_api_key = st.secrets.get("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY")

# ✅ Main backend function used in app.py
def careerbot_chat(prompt):
    if not openrouter_api_key:
        return "⚠️ API key for OpenRouter not found. Please set it in Streamlit secrets or environment."

    headers = {
        "Authorization": f"Bearer {openrouter_api_key}",
        "Content-Type": "application/json",
        "X-Title": "AI CareerBot"
    }

    messages = [
        {"role": "system", "content": "You are an AI career counselor helping users with career advice."},
        {"role": "user", "content": prompt}
    ]

    data = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 512
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"⚠️ Error: {e}"


# ✅ Compatibility-safe rerun
def safe_rerun():
    try:
        st.experimental_rerun()
    except AttributeError:
        from streamlit.runtime.scriptrunner import RerunException
        import streamlit.runtime.scriptrunner as scriptrunner
        raise RerunException(scriptrunner.RerunData(None))


# ✅ Optional UI function with enhanced design
def careerbot_ui():
    st.set_page_config(page_title="AI CareerBot", layout="wide")
    # Inject complete UI styling
    st.markdown("""
        <style>
        /* Universal font and spacing */
        html, body, [class*="css"]  {
            font-family: 'Segoe UI', sans-serif;
            font-size: 16px;
            line-height: 1.6;
        }

        /* Chat message container */
        .chat-container {
            max-height: 400px;
            overflow-y: auto;
            padding: 10px;
            border-radius: 10px;
            background-color: #f0f2f6;
            border: 1px solid #ccc;
            margin-bottom: 10px;
        }

        .chat-user {
            background-color: #d1e7dd;
            padding: 10px 14px;
            border-radius: 12px;
            margin: 8px 0;
            text-align: right;
            color: #000;
            max-width: 75%;
            margin-left: auto;
            font-size: 14px;
        }

        .chat-bot {
            background-color: #f8d7da;
            padding: 10px 14px;
            border-radius: 12px;
            margin: 8px 0;
            text-align: left;
            color: #000;
            max-width: 75%;
            margin-right: auto;
            font-size: 14px;
        }

        /* Input + button aligned */
        .input-row {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .stTextInput>div>div>input {
            height: 38px;
            padding: 6px 10px;
        }

        .stButton>button {
            height: 38px;
            padding: 0 20px;
            background-color: #1f77b4;
            color: white;
            border-radius: 6px;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        .stButton>button:hover {
            background-color: #145a86;
        }

        /* Dark Mode Support */
        body[data-theme="dark"] .chat-container {
            background-color: #1e1e1e;
            color: #ffffff;
            border: 1px solid #333;
        }

        body[data-theme="dark"] .chat-user {
            background-color: #344b36;
            color: #fff;
        }

        body[data-theme="dark"] .chat-bot {
            background-color: #5c2b2b;
            color: #fff;
        }
        </style>
    """, unsafe_allow_html=True)


    st.title("🤖 AI CareerBot - Your Smart Career Advisor")
    st.markdown("Ask anything about **careers, skills, tech paths, or job trends**. I'm here to help!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    def add_message(role, content):
        st.session_state.messages.append({"role": role, "content": content})
        if len(st.session_state.messages) > 30:
            st.session_state.messages = st.session_state.messages[-30:]

    def clear_chat():
        st.session_state.messages = []
        safe_rerun()

    with st.container():
        user_input = st.text_input("Ask your career question here:", key="user_input", placeholder="e.g., How to become a Data Scientist?")

        col1, col2 = st.columns([1, 5])
        with col1:
            send_btn = st.button("📨 Send")
        with col2:
            clear_btn = st.button("🧹 Clear Chat")

    if clear_btn:
        clear_chat()

    if send_btn and user_input.strip():
        add_message("user", user_input)

        placeholder = st.empty()
        placeholder.markdown("💬 _CareerBot is typing..._")

        reply = careerbot_chat(user_input)
        add_message("assistant", reply)

        placeholder.empty()
        safe_rerun()

    # Chat messages display
    with st.container():
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for msg in st.session_state.messages:
            role_class = "user-msg" if msg["role"] == "user" else "bot-msg"
            name = "You" if msg["role"] == "user" else "CareerBot"
            st.markdown(f"<div class='{role_class}'><b>{name}:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
