import subprocess
import re

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
    return f"""
[INST] <<SYS>>You are very helpful and obedient assistant. You should be a translator that converts human text to cli commands. Here your goal is to be present with a cli app and with your help convert human natural language into cli app commands. Below are some results of executing specific commands. Use the information about the cli app to answer based on user defined guidelines. You will follow the instructions very carefully and only answer with json responses. Your answer will change the state of tasks in the todo application, the current state will always be part of the prompt. You will never include explanation in your answer. You will use the examples for generating the command in your answer.<</SYS>>

Example correct usage of cli app usage, please pay attention to the examples below:
* Mark one task as done: `todo done 1` 
* Mark multiple tasks as done: `todo done 1 2 3`
* Add task: `todo add "Fix the window"`
* Add task with priority: `todo add "Fix the window" --priority 3`
* Update task priority using id: `todo task 2 --priority 2`
* Add task with context information: `todo add "Fix the window" --context "home"`
* Update task context using id: `todo task 2 --context "new_context"`
* Update two task's context using id: `todo task 2 --context "new_context"; todo task 1 --context "new_context"`

Strictly follow these guidelines for your answer:
1. Output should include a valid json with only one key `command` and value should be the command to be executed.
2. Output must only contain json.
3. Do not include explanation in your answer.

Hints:
1. You can perform multiple commands by separating them with a semicolon. For example: `todo done 1; todo task 2 -p 2`
2. By default all tasks have priority 1 and no context. Priorities range from 1-99 where 1 is the least priority and 99 is the most priority task.
3. Only one task can be updated at a time when updating priority or context of the task.

Answer JSON schema:
{{"command": "your command here"}}

Example answers:
* {{"command": "todo done 1"}} 
* {{"command": "todo add "Fix the window" --priority 3"}} 
* {{"command": "todo task 2 --priority 2"}}
* {{"command": "todo done 1; todo task 2 --priority 2"}}

Task:
Generate one cli command to perform the following task, use the examples above to generate the command. Try to think if the task is a single task or multiple tasks. If the task is a single task, generate a command for a single task. If the task is multiple tasks, generate a command for multiple tasks. Also verify the task id before generating the command. Consider if the positional are valid for the task. Focus on current state of the tasks and generate the command to achieve desired state. The task below could include task names or context information or priority information. Do not forget the hints provided above. Remember to not include any explanation in your answer.
"{task}"[/INST]
"""
