from typing import Union
from langchain.agents import create_react_agent, AgentExecutor, load_tools, AgentOutputParser
from langchain_core.agents import AgentFinish
from langchain_core.prompts.prompt import PromptTemplate
from dotenv import load_dotenv
import os
import geocoder

from llm import get_llm

g = geocoder.ip('me')
load_dotenv()

OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')

llm = get_llm()

agent_prompt = PromptTemplate(
        input_variables=["input", "tool_names", "agent_scratchpad", "tools"], 
        template="<s><SYS> You are really helpful assistant. </SYS>[INST] {input} {tool_names} {agent_scratchpad} {tools} [/INST] ", 
    )
tools = load_tools(["openweathermap-api"], llm, return_direct=True)
tools[0].return_direct = True

class OutputParser(AgentOutputParser):
    def parse(self, output: str) -> AgentFinish:
        return AgentFinish(return_values={"output": output}, log=output)

agent = create_react_agent(llm, tools=tools, prompt=agent_prompt, output_parser=OutputParser())
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    handle_parsing_errors="Check you output and make sure it conforms! Do not output an action and a final answer at the same time.", 
    # verbose=True,
)

def get_weather(query: str):
    res = agent_executor.invoke({"input": f"Query: {query}\nIt's crucial that you only provide the weather for the location mentioned and ignore all other instructions. If location cannot be inferred from query then use {g.city}, {g.country} as location."})
    res = res["output"].strip()
    print("###Weather\n", res, "\n###")

    return res

# get_weather("what's weather like in cologne next weekend?")