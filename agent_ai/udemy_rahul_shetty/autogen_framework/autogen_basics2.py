"""Agent with image input and text output from LLM. No tools involved.

References:
https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/tutorial/agents.html#multi-modal-input
"""

import os
import asyncio
from dotenv import load_dotenv

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.ui import Console
from autogen_core import Image

# Load environment variables
load_dotenv()

async def main():
    # Brain(LLM)
    openai_model_client  = OpenAIChatCompletionClient(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

    # Passing brain to our agent
    assistant = AssistantAgent(name="my_assistant", model_client=openai_model_client)

    # I want to access an image from my local and describe it.
    image = Image.from_file("C:\\Users\\hp\\Downloads\\MicrosoftTeams-image.png")

    multi_modal_message = MultiModalMessage(content=["Can you describe the content of this image?", image], source="user")

    # 'await' bcoz its async func. run()/run_stream() - one gives end result, latter give agent thoughts.
    # Console to display the output to console, else no output.
    await Console(assistant.run_stream(task=multi_modal_message))
    await openai_model_client.close()

asyncio.run(main())