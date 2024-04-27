import streamlit as st
from llm_generate import get_cmd, exec_commands  # Import functions from llm_generate

## Functions

def get_tasks():
  """
  Fetches and displays task data from a database connection.

  Returns:
      A pandas DataFrame containing task information (ID, title, context, priority, done status, start date).
  """
  conn = st.connection('main', type='sql')  # Establish a Streamlit database connection
  tasks = conn.query('select t.id, t.title, c.path as context, t.priority, iif(ifnull(t.done, false), \'true\', \'false\') done, t.start from Task t, Context c where t.context = c.id;', ttl=0)  # Query the database for tasks
  return tasks  # Return the retrieved task data as a DataFrame

## Streamlit Configuration

st.set_page_config(page_title="AI Assistant", page_icon="")  # Set page title and icon
st.title("Taskai")  # Display title for the Streamlit app

## Chatbot Initialization

greeting = "Hello! I am your AI Assistant. Here's how your tasks look like today:"

# Initialize an empty list for chat history if it doesn't exist in the session state
if "messages" not in st.session_state:
  st.session_state.messages = []

# Display past chat messages from session state
for message in st.session_state.messages:
  with st.chat_message(message["role"]):  # Use chat_message container for each message
    st.write(message["content"])  # Display message content

# Display greeting and task list initially
if len(st.session_state.messages) == 0:
  st.chat_message("assistant").write(greeting)  # Welcome message from assistant
  st.dataframe(get_tasks(), hide_index=True)  # Display initial task list

## User Interaction

if prompt := st.chat_input("How can I help you with the tasks?"):
  # Capture user input through chat_input
  with st.chat_message("user"):  # Display user message in chat container
    st.markdown(prompt)  # Format user input as markdown

  # Append the user's message to the chat history
  st.session_state.messages.append({"role": "user", "content": prompt})

  # Send the user's prompt to get_cmd for processing (potentially using RAG)
  cmd = get_cmd(prompt, True)
  res = f"Command executed: {cmd}"  # Prepare response string

  with st.chat_message("assistant"):  # Display assistant response in chat container
    if cmd != "":  # Check if a valid command was generated
      exec_commands(cmd)  # Execute the retrieved command
      st.write(res)  # Display confirmation message
      st.dataframe(get_tasks(), hide_index=True)  # Update task list
    else:
      res = "I'm sorry, I couldn't understand your request. Please try again with a different prompt."
      st.write(res)  # Display error message

  # Update chat history with assistant's response
  st.session_state.messages.append({"role": "assistant", "content": res})