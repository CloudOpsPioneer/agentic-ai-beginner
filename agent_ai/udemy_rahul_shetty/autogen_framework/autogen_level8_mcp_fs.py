"""Agent to Human interaction. Agent and Human talks with Termination condition as some Text pattern.
Additionally, Filesystem MCP is integrated.

References:
https://microsoft.github.io/autogen/stable//reference/python/autogen_ext.tools.mcp.html
"""

import os
import asyncio
from dotenv import load_dotenv

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import UserProxyAgent, AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench
from autogen_agentchat.ui import Console

# Load environment variables
load_dotenv()

async def main():
    # Brain(LLM)
    openai_model_client  = OpenAIChatCompletionClient(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))


    # Converting the config from below server as params
    # https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem#npx
    fs_server_params =  StdioServerParams(
         command="npx", args=["-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\hp\\Downloads"],
         read_timeout_seconds=60
     )

    # For multiple workbench ->
    # async with McpWorkbench(fs_server_params) as fs_wb, McpWorkbench(playwright_params) as pw _wb:
    async with McpWorkbench(fs_server_params) as fs_wb:

        # Note we are passing workbench param
        agent = AssistantAgent(name="Teacher", model_client=openai_model_client, workbench=fs_wb,
                                system_message="You are  an AI assistant. Keep everything not more than 2 sentences."
                                               "You can access the file system."
                                               "when users says 'THANKS DONE' or similar, acknowledge and say 'LESSON COMPLETE' to end session.")
        user_proxy = UserProxyAgent(name="Student")

        # Using RoundRobinGroupChat team from several other teams. Termination condition is 4 convos.
        team = RoundRobinGroupChat(participants=[user_proxy, agent], termination_condition=TextMentionTermination("LESSON COMPLETE"))

        await Console(team.run_stream(task="I need help with geography. Let's talk."))
    await openai_model_client.close()

asyncio.run(main())