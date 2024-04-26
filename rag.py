from llama_index.core import SummaryIndex
from llama_index.readers.weather import WeatherReader
from IPython.display import Markdown, display
import os

from dotenv import load_dotenv
load_dotenv()

OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
print(OPENWEATHERMAP_API_KEY)

documents = WeatherReader(token=OPENWEATHERMAP_API_KEY).load_data(["London", "New York", "Mumbai"])

print(documents)

