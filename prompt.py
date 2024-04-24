import subprocess
import re
import json

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

def create_prompt(task):
	f = open('prompts.json')
	data = json.load(f)

	prompt = ""
	prompt += f"<s>[INST] <<SYS>>\r\n{data['system_prompt'].strip()}\r\n<</SYS>>\r\n"
	prompt += f"{data['training'][0]['input'].strip()} [/INST] {data['training'][0]['reply'].strip()} </s>"

	for i in range(1, len(data["training"])):
		prompt += f"<s>[INST] {data['training'][i]['input'].strip()} [/INST] {data['training'][i]['reply'].strip()} </s>"

	last_prompt =  f"""
<s>[INST] Awesome, you are being really helpful. Let's try to use all we have learned until now. To recap the list of available commands are: ["done", "task", "add"]. Please remember to only include JSON in your answer. Another insight is that a high priority task is any task with priority greater than 1. Pay utmost focus on the task id because they are really important. The tasks on the app looks like this now:
ID | Title | Context | Priority
```
{exec_commands('todo search ""')}
```
Your goal is the following: {task} [/INST]
"""

	prompt += last_prompt

	return prompt