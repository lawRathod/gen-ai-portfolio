import os
from dotenv import load_dotenv
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from typing import Any, Optional
import requests
import json
from langchain_core.language_models.llms import LLM

# Load environment variables (likely contains AWS API Key)
load_dotenv()

# Access AWS API key from environment variables
AWS_API_KEY = os.getenv('AWS_API_KEY')


class AWS_LLM(LLM):
    """
    A class representing an LLM interface for AWS LLM (possibly LLAMA) service.
    """

    @property
    def _llm_type(self) -> str:
        """
        Returns a string identifying the type of LLM this class represents.
        """
        return "AWS_LLM_LLAMA"  # Replace with actual LLM name if different

    def _call(
        self,
        prompt: str,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """
        Sends a prompt to the AWS LLM service and returns the generated text.

        Args:
            prompt: The text prompt to send to the LLM.
            run_manager: (Optional) A callback manager for the LLM run (likely not used here).
            **kwargs: Additional keyword arguments (ignored in this implementation).

        Returns:
            The generated text response from the AWS LLM service.
        """

        body = {
            "prompt": prompt.strip(),
            "max_gen_len": 1024,
            "temperature": 0.01,
            "top_p": 1,
            "api_token": AWS_API_KEY,
        }

        # Send a POST request to the AWS LLM service endpoint
        res = requests.post(
            "https://6xtdhvodk2.execute-api.us-west-2.amazonaws.com/dsa_llm/generate",
            json=body,
        )

        # Parse the JSON response and return the generated text
        return json.loads(res.text)["body"]["generation"]


def get_llm():
    """
    Creates and returns an instance of the AWS_LLM class for interacting with the AWS LLM service.
    """
    llm = AWS_LLM()
    return llm
