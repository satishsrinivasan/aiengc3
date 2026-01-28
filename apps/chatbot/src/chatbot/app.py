import streamlit as st
import http_api

models = {
    "OpenAI": ["gpt-5-nano", "gpt-5-mini"],
    "Gemini": ["gemini-2.5-flash"],
    "Groq": ["llama-3.3-70b-versatile"]
}

st.title("Chatsaurus")

with st.sidebar:
    st.title("Settings")

    provider_name: str = st.selectbox("Provider", [key for key in models.keys()])
    model_name: str = st.selectbox("Model", models[provider_name])

    st.session_state.provider_name = provider_name
    st.session_state.model_name = model_name

if "conversation" not in st.session_state:
    st.session_state.conversation = [
        {"role": "assistant", "content": "Hello! How may I assist you today?"}
    ]

for message in st.session_state.conversation:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(st.session_state.conversation[0]["content"]):
    st.session_state.conversation.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        output = http_api.invoke_method(st.session_state, "post", "http://api:8000/chat",
            json={"provider_name": st.session_state.provider_name,
                  "model_name": st.session_state.model_name,
                  "messages": st.session_state.conversation
            })
        response_data = output[1]
        answer = response_data["message"]
        for line in answer.splitlines():
            st.write(line)
    st.session_state.conversation.append({"role": "assistant", "content": answer})

