"""This file will have all the agent defined, and return only the agent instance..."""

from autogen_agentchat.agents import AssistantAgent
from mcp_config import McpConfig

class AgentFactory:

    def __init__(self, model_client):
        self.model_client = model_client
        self.mcp_config = McpConfig


    def create_database_agent(self, system_message):
        db_agent = AssistantAgent(name="DatabaseAgent", model_client=self.model_client,
                                  workbench = self.mcp_config.get_mysql_workbench(),
                                  system_message=system_message)

        return db_agent


    # Give two tools capabilities to one agent
    def create_api_agent(self, system_message):
        api_agent = AssistantAgent(name="APIAgent", model_client=self.model_client,
                                  workbench = [ self.mcp_config.get_rest_api_workbench(), self.mcp_config.get_filesystem_workbench() ],
                                  system_message=system_message)

        return api_agent


    def create_excel_agent(self, system_message):
        excel_agent = AssistantAgent(name="ExcelAgent", model_client=self.model_client,
                                   workbench = self.mcp_config.get_excel_workbench(),
                                   system_message=system_message)

        return excel_agent
