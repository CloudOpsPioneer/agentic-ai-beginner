"""This file will have all the agent defined, and return only the agent instance..."""

from autogen_agentchat.agents import AssistantAgent
from mcp_config import McpConfig

class AgentFactory:

    def __init__(self, model_client):
        self.model_client = model_client
        self.mcp_config = McpConfig

    # Reusable generic database agent
    def create_database_agent(self, system_message):
        db_agent = AssistantAgent(name="DatabaseAgent", model_client=self.model_client,
                                  workbench = self.mcp_config.get_mysql_workbench(),
                                  system_message=system_message)

        return db_agent
