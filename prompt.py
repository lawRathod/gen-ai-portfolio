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
	system_prompt = "You are a very helpful and obedient assistant. You need act as a translator that converts human text to cli commands. You will use information provided to you to learn the usage of cli app. Remember that your output will be parsed as JSON text. Be precise and thoughtful in your response."
	training_prompts = [
		{
			"user": "Hello! I will be sending you a task that needs to be converted to a cli command. You will need to generate a cli command that will perform the task. The task will be related to a todo app."
			"ai": "Happy to help you, let's get started!" 
		},
		{
			"user": "",
			"ai": ""
		}
	]
    return f"""
<s>[INST] <<SYS>><</SYS>>

 [/INST]  </s><s>[INST] You will only respond with valid JSON text from here on. The cli app we want to use is called "todo". I will be sharing with you example usage to help you understand the commands. Let's start with command to add task. `todo add "Water the plants";`, this command adds a task called "Water the plants" with priority 1 and context "default". Since we didn't specify context/priority the defaults are used. The command with context/priority is: `todo add "Water the plants" --context home --priority 2;`. So far the state of app looks like this:
```
 2 | Water the plants ★2 #home
 1 | Water the plants
```
Here the first task has priority 2 and context "home". The second task has priority 1 and no context. The tasks are displayed with id, task name, priority, and context. The priority can range from 1-99 where 1 is the least priority and 99 is the most priority task. The context is a string that can be used to group tasks. With the description so far, let's try to create a task for you to convert to a cli command. 

Task: Create a todo task to iron clothes with high priority and relevant context. [/INST] {{"command": "todo add \\"Iron clothes\\" --priority 99 --context home;"}} </s><s>[INST] Nicely done, similarly to mark task as completed or done the command is: `todo done TASK_ID;`. To mark multiple tasks as done, the command should be: `todo done TASK_ID TASK_ID TASK_ID`. Let's test your knowledge now, how will you mark task first and third as completed? [/INST] Sure I will try to help. The command should be
{{"command": "task done 1 3;"}}
</s><s>[INST] Please never include anything other than the JSON in your response. [/INST]</s> {{"command": "task done 1 3;"}} <s>[INST] Nice job, you are doing a great job. Let's move on to more commands. The tasks on the app looks like this now: 
```
 1 | [DONE] LLM Homework #homework_list
 2 | NLP Homework #homework_list
 3 | [DONE] Math Homework #homework_list
 4 | ML Homework #homework_list
```
If you notice the tasks 1 and 3 are marked as done while task 2 and 4 are still pending. The context for all tasks is "homework_list". The next command is to update the task priority. The command to update task priority is: `todo task TASK_ID --priority PRIORITY;`. Let's say we want to update the priority of task 2 to 2. What will be the command? [/INST] {{"command": "todo task 2 --priority 2;"}} </s><s>[INST] Great job! You are doing fantastic. Let's move on to the next command. The tasks on the app looks like this now:
``` 
 1 | [DONE] LLM Homework #homework_list
 2 | NLP Homework ★2 #homework_list
 3 | [DONE] Math Homework #homework_list
 4 | ML Homework #homework_list
```
The next command is to update the task context. The command to update task context is: `todo task TASK_ID --context "CONTEXT";`. Let's say we want to update the context of task 4 to "work_list". What will be the command? [/INST] {{"command": "todo task 4 --context \\"work_list\\";"}} </s><s>[INST] Great! It's really amazing that you didn't forget to only include JSON. I hope you can continue to not include any other texts in all future responses. Let's learn how to chain commands to execute multiple. To perform two commands you can separate them with semicolon. Example: `todo task 2 --priority 2; todo task 3 --priority 99;`. Similarly how would you move task one and third to work_list? [INST] {{"command": "todo task 1 --context \\"work_list\\"; todo task 3 --context \\"work_list\\";"}} </s><s>[INST] Awesome, you are being really helpful. Let's try to use all we have learned until now. To recap the list of available commands are: ["done", "task", "add"]. Please remember to only include JSON in your answer. The tasks on the app looks like this now:
```
{exec_commands('todo search ""')}
```
Your goal is the following: {task} [/INST]
"""
