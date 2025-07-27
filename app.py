import streamlit as st
from openai import OpenAI

# ✅ Set your actual OpenRouter API key here
api_key = "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"  # Replace with your key from https://openrouter.ai/keys

# ✅ Initialize OpenAI client for OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# ✅ Streamlit UI setup
st.set_page_config(page_title="Search Chat Engine", layout="wide")
st.title("🧠 ChatGPT-like Search Engine using OpenRouter")

# ✅ Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ✅ User input
user_input = st.chat_input("Ask me anything about industrial components, etc.")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        # ✅ Call OpenRouter via OpenAI client
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://your-app-name.streamlit.app",  # Optional
                "X-Title": "Search Chat Engine",  # Optional
            },
            model="deepseek/deepseek-r1:free",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
        )
        response = completion.choices[0].message.content

    except Exception as e:
        response = f"❌ Error: {e}"

    # ✅ Show assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
