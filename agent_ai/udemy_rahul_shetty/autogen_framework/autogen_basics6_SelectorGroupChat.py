"""Three agents work on a given task and Terminate based on Text pattern or maximum of 10 convos.

References:
https://microsoft.github.io/autogen/stable//reference/python/autogen_agentchat.teams.html#autogen_agentchat.teams.SelectorGroupChat
"""

import os
import json
import asyncio
from dotenv import load_dotenv

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination

# Load environment variables
load_dotenv()

async def main():
    # Brain(LLM)
    openai_model_client  = OpenAIChatCompletionClient(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

    # Agents
    researcher = AssistantAgent(name="ResearcherAgent", model_client=openai_model_client, system_message="You are a researcher. Your role is to gather information and provide research findings only."
                                "Do not write articles or create content - just provide research data and facts in shorter format.")

    writer = AssistantAgent(name="WriterAgent", model_client=openai_model_client, system_message="You are a writer. Your role is to take research information and create well-written articles. Wait for research to be provided, then write the content.")

    critic = AssistantAgent(name="CriticAgent", model_client=openai_model_client, system_message="You are a critic. Review written content and provide feedback. Say 'TERMINATE' when satisfied with the final results.")

    # Terminate interaction of critic says TERMINATE else upto 10 convo. OR condition here.
    text_termination = TextMentionTermination('TERMINATE')
    max_msg_termination = MaxMessageTermination(max_messages=10)
    termination = text_termination | max_msg_termination

    # Order of participants are not necessary unlike RoundRobinGroupChat()
    # Allowing same agent to interact again - allow_repeated_speaker
    team = SelectorGroupChat(participants=[critic, writer, researcher], model_client=openai_model_client,
                             termination_condition=termination, allow_repeated_speaker=True)

    await Console(team.run_stream(task="Research renewable energy trends and write a brief article about the future of solar power."))
    await openai_model_client.close()

asyncio.run(main())