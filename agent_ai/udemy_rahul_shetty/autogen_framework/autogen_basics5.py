"""One agent shares memory to another agent.

References:
https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/tutorial/state.html
"""

import os
import json
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

    # Two agents
    agent1 = AssistantAgent(name="Helper", model_client=openai_model_client)
    agent2 = AssistantAgent(name="BackupHelper", model_client=openai_model_client)

    # Interacting with Agent1 and saving state
    await Console(agent1.run_stream(task="My favourite movie is Ironman"))
    state = await agent1.save_state()
    with open('memory.json', 'w') as f:
        json.dump(state, f, default=str)

    # Loading the saved state and passing to another agent
    with open('memory.json', 'r') as f:
        saved_state = json.load(f)

    await agent2.load_state(saved_state)
    await Console(agent2.run_stream(task="Tell me something that I love."))
    await openai_model_client.close()

asyncio.run(main())