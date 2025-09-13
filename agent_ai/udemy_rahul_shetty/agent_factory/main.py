import os
import asyncio
from dotenv import load_dotenv

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.ui import Console

from agent_factory import AgentFactory


load_dotenv()


async def main():
    # Brain(LLM)
    model_client  = OpenAIChatCompletionClient(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

    # object of the class, and passing the args to constructor
    factory = AgentFactory(model_client)

    db_agent = factory.create_database_agent(system_message=("""You are database agent. 
                        Understand the tables and the data first.
                        Read the items with price in descending order and pass the information to api agent."""))

    api_agent = factory.create_api_agent(system_message=("You are an API agent and filesystem agent. You have full permission to the local path. Do the file operations in the path you have permissions to as per the instruction given by database agent"))

    excel_agent = factory.create_excel_agent(system_message=("You are an Excel agent. Receive the data from database agent and write to excel file, and say COMPLETE"))

    teams = RoundRobinGroupChat(participants=[db_agent, api_agent],
                        termination_condition=TextMentionTermination("COMPLETE"))

    await Console(teams.run_stream(task="Read the database and write to text file. Hit the endpoint https://api.restful-api.dev/objects and write this too"))

    await model_client.close()



asyncio.run(main())