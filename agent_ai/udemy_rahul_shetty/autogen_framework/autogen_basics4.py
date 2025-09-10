"""Agent to Human interaction. Agent and Human talks with Termination condition as some Text pattern.

References:
https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/tutorial/teams.html
https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/tutorial/human-in-the-loop.html
https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/tutorial/termination.html

Refer examples here
https://microsoft.github.io/autogen/stable//reference/python/autogen_agentchat.teams.html#autogen_agentchat.teams.RoundRobinGroupChat
"""

import os
import asyncio
from dotenv import load_dotenv

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import UserProxyAgent, AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.ui import Console

# Load environment variables
load_dotenv()

async def main():
    # Brain(LLM)
    openai_model_client  = OpenAIChatCompletionClient(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

    # Two agents - Teacher & Student
    agent = AssistantAgent(name="Teacher", model_client=openai_model_client,
                            system_message="You are a maths teacher, Explain concepts shortly. Keep everything not more than 2 sentences."
                                           "when users says 'THANKS DONE' or similar, acknowledge and say 'LESSON COMPLETE' to end session."
                                           "Don't answer if the question is not related to maths")
    user_proxy = UserProxyAgent(name="Student")

    # Using RoundRobinGroupChat team from several other teams. Termination condition is 4 convos.
    team = RoundRobinGroupChat(participants=[user_proxy, agent], termination_condition=TextMentionTermination("LESSON COMPLETE"))

    await Console(team.run_stream(task="I need help with geography. Let's talk."))
    await openai_model_client.close()

asyncio.run(main())