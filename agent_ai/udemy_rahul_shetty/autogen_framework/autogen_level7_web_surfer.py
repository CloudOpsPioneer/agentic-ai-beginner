"""Webserver Automation

References:
https://microsoft.github.io/autogen/stable//reference/python/autogen_ext.agents.web_surfer.html#autogen_ext.agents.web_surfer.MultimodalWebSurfer

Note:
- Install this module before running the script, else it will ask you to do.
    pip3 install playwright
- It will ask you to run
    playwright install
"""

import os
import json
import asyncio
from dotenv import load_dotenv

from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.agents.web_surfer import MultimodalWebSurfer

# Load environment variables
load_dotenv()

async def main():
    # Brain(LLM)
    openai_model_client  = OpenAIChatCompletionClient(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

    # Agents
    web_surfer_agent = MultimodalWebSurfer(
        name="WebSurfer", model_client=openai_model_client, headless=False, animate_actions=True)

    agent_team = RoundRobinGroupChat(participants=[web_surfer_agent], max_turns=5)

    await Console(agent_team.run_stream(task="Navigate to apple.com and check the latest iPhone price and spec. Summarize it."))
    await web_surfer_agent.close()
    await openai_model_client.close()

asyncio.run(main())