import streamlit as st
import requests
import json
from prompt import create_prompt, exec_commands

## functions
def llama_generate(prompt):
    final_prompt = create_prompt(prompt)
    print("*****\n", final_prompt, "\n*****")
    url = 'https://6xtdhvodk2.execute-api.us-west-2.amazonaws.com/dsa_llm/generate'
    body = {
        "prompt": final_prompt.strip(),
        "max_gen_len": 100,
        "temperature": 0.01,
        "top_p": 1,
        "api_token": st.secrets["AWS_API_KEY"],
    }
    res = requests.post(url,  json = body)
    out = json.loads(res.text)["body"]["generation"]
    out = out.strip()
    try:
        outputjs = json.loads(out)
        cmd = outputjs["command"]
        if cmd != "":
            return cmd
    except:
        print("###\n", repr(out), "\n###")
        return ""

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

    # res = get_tasks()
    cmd = llama_generate(prompt)
    res = f"Command executed: {cmd}"

    with st.chat_message("assistant"):
        if cmd != "":
            exec_commands(cmd)
            st.write(res)
            st.dataframe(get_tasks())
        else:
            res = "I'm sorry, I couldn't understand your request. Please try again with different prompt."
            st.write(res)
    st.session_state.messages.append({"role": "assistant", "content": res})
        