import json
import subprocess
import re

from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
from llm import get_llm
from rag import get_weather

# utils functions
def exec_commands(commands):    
    p = subprocess.run(["bash", "-c", commands], capture_output=True, text=True)
    ansi_escape = re.compile(r'''
    \x1B  # ESC
    (?:   # 7-bit C1 Fe (except CSI)
        [@-Z\\-_]
    |     # or [ for CSI, followed by a control sequence
        \[
        [0-?]*  # Parameter bytes
        [ -/]*  # Intermediate bytes
        [@-~]   # Final byte
    )
''', re.VERBOSE)
    return ansi_escape.sub('', p.stdout)

def final_cli_prompt_template(prompt: str): 
    temp = f"""
Awesome, you are being really helpful. Let's try to use all we have learned until now. 
To recap the list of available commands are: ["done", "task", "add", "rm"].
Please remember to only include JSON in your answer without any reason , format: `{{\"command\": \"YOUR_COMMAND\"}}`. Also remember that a high priority task is any task with priority greater than 1. 
Pay utmost focus on the task id because they are really important. A task id is a number/alphabet that is unique to each task.

The tasks on the app looks like this now, make sure to use all information available to you to complete the task:
ID | Title | Context | Priority
```
{exec_commands('todo search ""')}
```
Your goal is the following: {prompt}
Additional information:
Datetime now: {exec_commands('date')}
    """
    return temp.strip()

def final_explain_prompt_template(prompt: str, weather: bool = False): 
    temp = f"""
Awesome, you are being really helpful. Let's try to use all we have learned until now. 
Pay utmost focus on the task id because they are really important. A task id is a number/alphabet that is unique to each task.
You will not produce commands or examples, only explain what needs to be done in general tone. Keep your explanation 1 statement long.
Remember not to update context unless asked explicitly in the task.
Always only use the commands you have learned and try not to invent new commands.

The tasks on the app looks like this now, make sure to use all information available to you to complete the task:
ID | Title | Context | Priority
```
{exec_commands('todo search ""')}
```
Task: {prompt}
    """
    if weather:
        temp += f"""
Additional information:
Datetime now: {exec_commands('date')}
Weather for next seven days: {get_weather(prompt)}"""

    return temp.strip()

def create_few_shot_template(data: dict):
  """
  Creates a FewShotPromptTemplate object based on provided data.

  Args:
      data: A dictionary containing training examples and system prompt information.
          - data["training"]: A list of dictionaries representing training examples.
              - Each dictionary in "training" should have "input" and "reply" keys.
          - data["system_prompt"]: The system prompt used for all training examples.

  Returns:
      A FewShotPromptTemplate object constructed from the provided data.
  """

  # Define a base prompt template with input and reply variables
  base_prompt = PromptTemplate(
      input_variables=["input", "reply"],
      template="<s>[INST] {input} [/INST] {reply} </s>",
  )

  # Create a FewShotPromptTemplate using the base prompt, training examples, and system prompt
  few_shot_template = FewShotPromptTemplate(
      examples=data["training"][1:],  # Exclude the first example from examples
      example_prompt=base_prompt,
      suffix="<s>[INST] {input} [/INST]",  # Suffix for subsequent examples
      example_separator="",  # No separator between examples
      prefix=f"<s>[INST] <<SYS>>\r\n{data['system_prompt']}\r\n<</SYS>>\r\n{data['training'][0]['input']} [/INST] {data['training'][0]['reply']} </s>",  # Prefix with system prompt and first example
      input_variables=["input"],  # Input variable for the final prompt
  )

  return few_shot_template

# Load examples from JSON files
f = open('cli_prompts.json')
cli_examples = json.load(f)

def cli_prompt(prompt: str) -> str:
  """
  Generates a command for the CLI interface using a few-shot prompt and LLM.

  Args:
      prompt: The user's goal or task description.

  Returns:
      The generated command string from the LLM.
  """

  # Create a few-shot template for CLI prompts using pre-loaded examples
  cli_command_prompt = create_few_shot_template(cli_examples)

  # Generate a final prompt by combining the CLI prompt template with the user's prompt
  final_prompt = cli_command_prompt.format(input=final_cli_prompt_template(prompt))

  # Invoke the LLM to get the response for the final prompt
  return get_llm().invoke(final_prompt)

f = open('explain_prompts.json')
explain_examples = json.load(f)

def explain_prompt(prompt: str, rag_enabled=False) -> str:
  """
  Generates an explanation prompt for the user's goal or task using a few-shot prompt and LLM.

  Args:
      prompt: The user's goal or task description.
      rag_enabled: (Optional) A flag indicating whether to use RAG for additional context (likely not used here).

  Returns:
      The generated explanation string from the LLM.
  """

  # Create a few-shot template for explanation prompts using pre-loaded examples
  explain_command_prompt = create_few_shot_template(explain_examples)

  # Generate a final prompt by combining the explanation prompt template with the user's prompt and optional RAG flag
  final_prompt = explain_command_prompt.format(input=final_explain_prompt_template(prompt, rag_enabled))

  # Invoke the LLM to get the response for the final prompt
  return get_llm().invoke(final_prompt)    

def get_cmd(prompt, rag=False):
  """
  Extracts a command for the CLI interface from a user prompt.

  Args:
      prompt: The user's goal or task description.
      rag: (Optional) A flag indicating whether to use RAG for additional context (likely not used here).

  Returns:
      The extracted command string from the LLM's response.

  Raises:
      Exception: If an invalid command is extracted.
  """

  # Generate an explanation for the user's prompt
  explanation = explain_prompt(prompt, rag)
  print("###Explanation\n", explanation, "\n###")

  # Generate a command for the CLI interface based on the explanation
  out = cli_prompt(explanation)

  # Remove any leading or trailing whitespace from the output
  cmd_json = out.strip()

  try:
    # Parse the output as JSON
    outputjs = json.loads(cmd_json)

    # Extract the "command" field from the JSON
    cmd = outputjs["command"]

    if cmd != "":
      # Print the extracted command
      print("###Command\n", cmd, "\n###")
      return cmd

  except:
    # Handle invalid JSON or missing "command" field
    print("###Invalid Command\n", repr(cmd_json), "\n###")
    raise Exception("Invalid command")