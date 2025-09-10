### Setup
- https://microsoft.github.io/autogen/stable//index.html
- Agent Chat: https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/index.html
- Follow and install: https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/installation.html

- Install pip packages as mentioned.
```shell
pip install -U "autogen-agentchat"
pip install "autogen-ext[openai]"
```

- Brain(LLM pkg) has been installed. Now for Tools, we are going to use mcp out of different tools mentioned here :
  - https://microsoft.github.io/autogen/stable//user-guide/extensions-user-guide/index.html
  - https://microsoft.github.io/autogen/stable//reference/python/autogen_ext.tools.mcp.html#autogen_ext.tools.mcp.mcp_server_tools
```shell
pip install -U "autogen-ext[mcp]"
```