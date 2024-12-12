from ollama import Client
import streamlit as st

# HTTP_PROXY_URL = os.environ["HTTP_PROXY_URL"]


OLLAMA_ENDPOINT = st.secrets["OLLAMA_ENDPOINT"]
print(OLLAMA_ENDPOINT)

def get_text_stream(stream):
    for chunk in stream:
        yield chunk['message']['content']

st.subheader("A simple chat app powered by Qwen2.5:3b")

client = Client(
  host = OLLAMA_ENDPOINT
)


if "messages" not in st.session_state:
    st.session_state.messages = []


# show history messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Your message here...?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)


    stream = client.chat(model='qwen2.5:3b', messages=st.session_state.messages, stream=True,)
    text_stream = get_text_stream(stream)
    with st.chat_message("assistant"):
        response = st.write_stream(text_stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
