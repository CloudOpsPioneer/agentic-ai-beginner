"""Agent with simple input and output from LLM. No tools involved.

References:
https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/quickstart.html
https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/tutorial/models.html#openai
https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/tutorial/agents.html#assistant-agent
"""

import os
import asyncio
from dotenv import load_dotenv

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console

# Load environment variables
load_dotenv()

async def main():
    # Brain(LLM)
    openai_model_client  = OpenAIChatCompletionClient(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

    # Passing brain to our agent
    assistant = AssistantAgent(name="my_assistant", model_client=openai_model_client)

    # 'await' bcoz its async func. run()/run_stream() - one gives end result, latter give agent thoughts.
    # Console to display the output to console, else no output.
    await Console(assistant.run_stream(task="What is capital of Canada?"))
    await openai_model_client.close()

asyncio.run(main())