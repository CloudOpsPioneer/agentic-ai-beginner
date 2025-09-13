import os
import asyncio
from dotenv import load_dotenv

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console

from agent_factory import AgentFactory

async def main():
    # Brain(LLM)
    model_client  = OpenAIChatCompletionClient(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

    # object of the class, and passing the args to constructor
    factory = AgentFactory(model_client)

    db_agent = factory.create_database_agent("You are database specialist")

