# Import libraries from langchain
from langchain.agents import create_react_agent, AgentExecutor, load_tools, AgentOutputParser
from langchain_core.agents import AgentFinish
from langchain_core.prompts.prompt import PromptTemplate

# Import libraries for environment variables and location
from dotenv import load_dotenv
import os
import geocoder

# Import custom LLM function
from .llm import get_llm

# Get user location using IP address
g = geocoder.ip('me')

# Load environment variables (likely contains API key)
load_dotenv()

# Access OpenWeatherMap API key from environment variables
OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')

# Get access to the large language model (LLM)
llm = get_llm()

# Define the prompt template for the agent
agent_prompt = PromptTemplate(
    input_variables=["input", "tool_names", "agent_scratchpad", "tools"],
    template="<s><SYS> You are really helpful assistant. </SYS>[INST] {input} {tool_names} {agent_scratchpad} {tools} [/INST] ",
)

# Load tools (likely the OpenWeatherMap API wrapper)
tools = load_tools(["openweathermap-api"], llm, return_direct=True)

# Set tool to return direct output
tools[0].return_direct = True

# Define a class to parse the agent's output
class OutputParser(AgentOutputParser):
    def parse(self, output: str) -> AgentFinish:
        # Return the agent's output and log it
        return AgentFinish(return_values={"output": output}, log=output)

# Create the agent with LLM, tools, prompt, and output parser
agent = create_react_agent(llm, tools=tools, prompt=agent_prompt, output_parser=OutputParser())

# Create an agent executor to manage interactions with the agent
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    handle_parsing_errors="Check your output and make sure it conforms! Do not output an action and a final answer at the same time.",
    # verbose=True,  # Uncomment for more detailed execution logs
)

# Function to get weather information
def get_weather(query: str):
    # Craft the input for the agent, including the query
    input_text = f"Query: {query}\nIt's crucial that you only provide the weather for the location mentioned and ignore all other instructions. If location cannot be inferred from query then use {g.city}, {g.country} as location."

    # Run the agent and get the response
    res = agent_executor.invoke({"input": input_text})

    # Extract and clean the response
    res = res["output"].strip()

    # Print the weather information
    print("###Weather\n", res, "\n###")

    # Return the weather data (optional)
    return res

# Example usage (can be commented out)
# get_weather("what's weather like in cologne next weekend?") get_weather("what's weather like in cologne next weekend?")