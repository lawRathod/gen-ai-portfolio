import os
from dotenv import load_dotenv
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from typing import Any, Optional
import requests
import json
from langchain_core.language_models.llms import LLM

load_dotenv()

AWS_API_KEY = os.getenv('AWS_API_KEY')

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
          "max_gen_len": 1024,
          "temperature": 0.01,
          "top_p": 1,
          "api_token": AWS_API_KEY
        }
        res = requests.post("https://6xtdhvodk2.execute-api.us-west-2.amazonaws.com/dsa_llm/generate",  json = body)
        return  json.loads(res.text)["body"]["generation"]

def get_llm():
    llm = AWS_LLM()
    return llm
