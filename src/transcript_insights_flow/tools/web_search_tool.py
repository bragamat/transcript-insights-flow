
import os
import json
from crewai import Any
import requests
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class WebSearchToolInput(BaseModel):
    """Input schema for MyCustomTool."""

    query: str = Field(..., description="Query to search the web for.")


class WebSearchTool(BaseTool):
    name: str = "WebSearchTool"
    description: str = (
        "A tool that allows the agent to search the web for information based on a query."
    )
    args_schema: Type[BaseModel] = WebSearchToolInput

    def _run(self, query: str) -> str:
        url = "https://google.serper.dev/search"
        payload = json.dumps({ "q": query })

        headers = {
          'X-API-KEY': os.getenv("SERPER_API_KEY"),
          'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)


        # Implementation goes here
        return self._format_result(response.text) # type: ignore

    def _format_result(self, result: list) -> list[Any]: # type: ignore
        res = [links.get('link') for links in json.loads(result).get("organic", [])] # type: ignore
        
        # Optional: Implement any result formatting if needed
        # {
        #   "organic": [
        #     {
        #       "title": "CrewAI: The AI Platform for Building Intelligent Applications",
        #       "link": "https://crewai.com/",
        #       "snippet": "CrewAI is an AI platform that enables developers to build Intelligent Applications with ease. It provides tools and infrastructure to create, deploy, and manage AI-powered applications efficiently."
        #     }
    #     ]
    # }

        return res



if __name__ == "__main__":
    tool = WebSearchTool()
    result = tool._run("What is CrewAI?")
    print(result)
