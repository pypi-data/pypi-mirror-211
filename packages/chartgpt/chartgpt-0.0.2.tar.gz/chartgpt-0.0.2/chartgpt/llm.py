import os
import re
from typing import Any, Dict, Optional

import openai

from .constants import END_CODE_TAG, START_CODE_TAG
from .prompts.base import Prompt

# from abc import ABC, abstractmethod


class LLM:
    def __init__(
        self,
        temperature: int = 0.2,
        model_name: str = "text-davinci-003",
        max_tokens: int = 1000,
    ):
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = 1
        self.frequency_penalty = 0
        self.presence_penalty = 0

    def _extract_code(self, response: str, separator: str = "```") -> str:
        """
        Extract the code from the response.

        Args:
            response (str): Response
            separator (str, optional): Separator. Defaults to "```".

        Raises:
            NoCodeFoundError: No code found in the response

        Returns:
            str: Extracted code from the response
        """
        code = response
        match = re.search(
            rf"{START_CODE_TAG}(.*)({END_CODE_TAG}|{END_CODE_TAG.replace('<', '</')})",
            code,
            re.DOTALL,
        )
        if match:
            code = match.group(1).strip()
        if len(code.split(separator)) > 1:
            code = code.split(separator)[1]
        print(code)

        return code

    def generate_code(self, instruction: Prompt, prompt: str) -> str:
        """
        Generate the code based on the instruction and the given prompt.

        Returns:
            str: Code
        """

        prompt = str(instruction) + prompt

        return self._extract_code(
            self.completion(prompt)
        )

    @property
    def _default_params(self) -> Dict[str, Any]:

        """
        Get the default parameters for calling OpenAI API

        Returns (Dict): A dict of OpenAi API parameters

        """

        return {
            "model": "text-davinci-003",
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
        }

    def completion(self, prompt: str) -> str:
        """
        Query the completion API

        Args:
            prompt (str): Prompt

        Returns:
            str: LLM response
        """
        params = {**self._default_params, "prompt": prompt}

        response = openai.Completion.create(**params)

        return response["choices"][0]["text"]
