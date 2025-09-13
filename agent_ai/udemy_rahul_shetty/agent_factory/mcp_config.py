
from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench

class McpConfig:

    def __init__(self):


    #https://github.com/designcomputer/mysql_mcp_server
    def get_mysql_workbench(self):
        mysql_server_params =  StdioServerParams(
            command="uv", args=["--directory", "C:\\Users\\hp\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages",
                                "run", "mysql_mcp_server"],
            env = {
                "MYSQL_HOST": "localhost",
                "MYSQL_PORT": "3306",
                "MYSQL_USER": "root",
                "MYSQL_PASSWORD": "123456789gt@",
                "MYSQL_DATABASE": "test_ecommerce"
            },
            read_timeout_seconds=60
        )

        return McpWorkbench(server_params=mysql_server_params)
