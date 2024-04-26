from typing import Any, List, Mapping, Optional

import requests
import json
import subprocess
import re

from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
from langchain.agents import load_tools, create_react_agent, AgentExecutor
from langchain import hub, memory
import os
from dotenv import load_dotenv

load_dotenv()

AWS_API_KEY = os.getenv('AWS_API_KEY')
OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')

class AWS_LLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "AWS_LLM_LLAMA"

    def _call(
        self,
        prompt: str,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        body = {
          "prompt": prompt.strip(),
          "max_gen_len": 512,
          "temperature": 0.01,
          "top_p": 1,
          "api_token": AWS_API_KEY
        }
        res = requests.post("https://6xtdhvodk2.execute-api.us-west-2.amazonaws.com/dsa_llm/generate",  json = body)
        return  json.loads(res.text)["body"]["generation"]

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

def final_prompt_template(prompt: str): 
    temp = f"""
Awesome, you are being really helpful. Let's try to use all we have learned until now. To recap the list of available commands are: ["done", "task", "add"]. Please remember to only include JSON in your answer. Another insight is that a high priority task is any task with priority greater than 1. Pay utmost focus on the task id because they are really important. The tasks on the app looks like this now:
ID | Title | Context | Priority
```
{exec_commands('todo search ""')}
```
Your goal is the following: {prompt}
    """
    return temp.strip()

f = open('cli_prompts.json')
examples = json.load(f)
def generate(prompt: str) -> str:
    llm = AWS_LLM()
    example_prompt = PromptTemplate(
        input_variables=["input", "reply"], 
        template="<s>[INST] {input} [/INST] {reply} </s>", 
    )

    cli_command_prompt = FewShotPromptTemplate(
        examples=examples["training"][1:],
        example_prompt=example_prompt,
        suffix="<s>[INST] {input} [/INST]",
        example_separator="",
        prefix= f"<s>[INST] <<SYS>>\r\n{examples['system_prompt']}\r\n<</SYS>>\r\n{examples['training'][0]['input']} [/INST] {examples['training'][0]['reply']} </s>",
        input_variables=["input"],
    )

    final_prompt = cli_command_prompt.format(input=final_prompt_template(prompt))
    
    return llm.invoke(final_prompt)

 

def get_cmd(prompt):
    out = generate(prompt)
    cmd_json = out.strip()

    try:
        outputjs = json.loads(cmd_json)
        cmd = outputjs["command"]
        if cmd != "":
            return cmd
    except:
        print("###\n", repr(cmd_json), "\n###")
        raise Exception("Invalid command")