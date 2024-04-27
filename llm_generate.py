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
    base_prompt = PromptTemplate(
        input_variables=["input", "reply"], 
        template="<s>[INST] {input} [/INST] {reply} </s>", 
    )

    few_shot_template = FewShotPromptTemplate(
        examples=data["training"][1:],
        example_prompt=base_prompt,
        suffix="<s>[INST] {input} [/INST]",
        example_separator="",
        prefix= f"<s>[INST] <<SYS>>\r\n{data['system_prompt']}\r\n<</SYS>>\r\n{data['training'][0]['input']} [/INST] {data['training'][0]['reply']} </s>",
        input_variables=["input"],
    )

    return few_shot_template

f = open('cli_prompts.json')
cli_examples = json.load(f)
def cli_prompt(prompt: str) -> str:
    cli_command_prompt = create_few_shot_template(cli_examples)
    final_prompt = cli_command_prompt.format(input=final_cli_prompt_template(prompt))

    return get_llm().invoke(final_prompt)

f = open('explain_prompts.json')
explain_examples = json.load(f)
def explain_prompt(prompt: str, rag_enabled = False) -> str:
    explain_command_prompt = create_few_shot_template(explain_examples)
    final_prompt = explain_command_prompt.format(input=final_explain_prompt_template(prompt, rag_enabled))

    return get_llm().invoke(final_prompt)

    
def get_cmd(prompt, rag = False):
    explanation = explain_prompt(prompt, rag)
    print("###Explanation\n", explanation, "\n###")
    out = cli_prompt(explanation)
    cmd_json = out.strip()

    try:
        outputjs = json.loads(cmd_json)
        cmd = outputjs["command"]
        if cmd != "":
            print("###Command\n", cmd, "\n###")
            return cmd
    except:
        print("###Invalid Command\n", repr(cmd_json), "\n###")
        raise Exception("Invalid command")