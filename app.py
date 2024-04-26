import streamlit as st
import requests
import json
from llm_generate import get_cmd, exec_commands
# from bokeh.models.widgets import Button
# from bokeh.models import CustomJS
# from streamlit_bokeh_events import streamlit_bokeh_events

## functions
def get_tasks():
    # Query and display the data you inserted
    conn = st.connection('main', type='sql')
    tasks = conn.query('select t.id, t.title, c.path as context, t.priority, iif(ifnull(t.done, false), \
                       \'true\', \'false\') done, t.start from Task t, Context c where t.context = c.id;', ttl=0)
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
    st.dataframe(get_tasks(), hide_index=True)

if prompt := st.chat_input("How can I help you with the tasks?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # res = get_tasks()
    cmd = get_cmd(prompt)
    res = f"Command executed: {cmd}"

    with st.chat_message("assistant"):
        if cmd != "":
            exec_commands(cmd)
            st.write(res)
            st.dataframe(get_tasks(), hide_index=True)
        else:
            res = "I'm sorry, I couldn't understand your request. Please try again with different prompt."
            st.write(res)
    st.session_state.messages.append({"role": "assistant", "content": res})
        
# STT
# stt_button = Button(label="Speak", width=100)

# stt_button.js_on_event("button_click", CustomJS(code="""
#     var recognition = new webkitSpeechRecognition();
#     recognition.continuous = true;
#     recognition.interimResults = true;
 
#     recognition.onresult = function (e) {
#         var value = "";
#         for (var i = e.resultIndex; i < e.results.length; ++i) {
#             if (e.results[i].isFinal) {
#                 value += e.results[i][0].transcript;
#             }
#         }
#         if ( value != "") {
#             document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
#         }
#     }
#     recognition.start();
#     """))

# result = streamlit_bokeh_events(
#     stt_button,
#     events="GET_TEXT",
#     key="listen",
#     refresh_on_update=False,
#     override_height=75,
#     debounce_time=0)

# if result:
#     if "GET_TEXT" in result:
#         st.write(result.get("GET_TEXT"))