import streamlit as st
from openai import OpenAI

# Load API key securely
api_key =""

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

st.title("🔍 OpenRouter Chat Search Engine")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

for msg in st.session_state.messages[1:]:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Ask something...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://<your-deployed-streamlit-url>",  # Optional
                "X-Title": "OpenRouter Chat Search",  # Optional
            },
            model="deepseek/deepseek-r1:free",
            messages=st.session_state.messages,
        )

        reply = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)

    except Exception as e:
        st.error(f"❌ Error: {e}")
