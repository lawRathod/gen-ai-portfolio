import streamlit as st
import subprocess
import re
import requests
import json
from streamlit.connections import SQLConnection

## functions
def llama_generate(prompt,
                   api_token,
                   max_gen_len = 512,
                   temperature = 0.01,
                   top_p =1):
  url = 'https://6xtdhvodk2.execute-api.us-west-2.amazonaws.com/dsa_llm/generate'
  body = {
    "prompt": prompt,
    "max_gen_len": max_gen_len,
    "temperature": temperature,
    "top_p": top_p,
    "api_token": api_token
  }
  res = requests.post(url,  json = body)
  return  json.loads(res.text)["body"]["generation"]

def get_tasks():
    # Query and display the data you inserted
    conn = st.connection('main', type='sql')
    tasks = conn.query('select * from Task;', ttl=0)
    return tasks


## Streamlit

st.set_page_config(page_title="AI Assistant", page_icon="🤖")
st.title("Taskai")

greeting = "Hello! I am your AI Assistant. Here's how your tasks look like today:"

## Chatbot
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if len(st.session_state.messages) == 0:
    st.chat_message("assistant").write(greeting)
    st.dataframe(get_tasks())

if prompt := st.chat_input("How can I help you with the tasks?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    res = get_tasks()
    # st.chat_message("assistant").write(llama_generate(prompt, st.secrets["AWS_API_KEY"]))
    with st.chat_message("assistant"):
        st.write(res)
    st.session_state.messages.append({"role": "assistant", "content": res})
        