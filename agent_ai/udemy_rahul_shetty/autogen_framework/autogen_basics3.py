"""Agent to Agent conversation. Two agents talk to each other with Termination condition.

Teacher & Student agent converse until the max msg termination condition is met.

References:
https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/tutorial/teams.html
https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/tutorial/human-in-the-loop.html
https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/tutorial/termination.html
"""

import os
import asyncio
from dotenv import load_dotenv

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.ui import Console

# Load environment variables
load_dotenv()

async def main():
    # Brain(LLM)
    openai_model_client  = OpenAIChatCompletionClient(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

    # Two agents - Teacher & Student
    agent1 = AssistantAgent(name="Teacher", model_client=openai_model_client,
                            system_message="You are a teacher, Explain concepts briefly and ask follow-up questions. Keep everything not more than 2 sentence.")
    agent2 = AssistantAgent(name="Student", model_client=openai_model_client,
                            system_message="You are a curious student. Ask questions and show your thinking process. Keep everything not more than 2 sentence.")

    # Using RoundRobinGroupChat team from several other teams. Termination condition is 4 convos.
    team = RoundRobinGroupChat(participants=[agent1, agent2], termination_condition=MaxMessageTermination(max_messages=4))

    await Console(team.run_stream(task="Let's discuss about beauty of Montreal."))
    await openai_model_client.close()

asyncio.run(main())