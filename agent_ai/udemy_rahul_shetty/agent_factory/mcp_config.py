
from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench

class McpConfig:


    # https://github.com/designcomputer/mysql_mcp_server
    # https://github.com/CloudOpsPioneer/agentic-ai-beginner/blob/main/agent_ai/udemy_rahul_shetty/claude_desktop_mcp/REAME.md
    @staticmethod
    def get_mysql_workbench():
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


    # https://github.com/dkmaker/mcp-rest-api
    # API example -> https://restful-api.dev/
    @staticmethod
    def get_rest_api_workbench():
        rest_api_server_params = StdioServerParams(
            command="npx", args=[ "-y", "dkmaker-mcp-rest-api" ],
            env = {
                "REST_BASE_URL": "https://api.restful-api.dev",
                "HEADER_Accept": "application/json"
            },
            read_timeout_seconds=60
        )

        return McpWorkbench(server_params=rest_api_server_params)


    # https://github.com/negokaz/excel-mcp-server
    @staticmethod
    def get_excel_workbench():
        excel_server_params = StdioServerParams(
            command="npx", args=[ "--yes", "@negokaz/excel-mcp-server" ],
            env = {
                "EXCEL_MCP_PAGING_CELLS_LIMIT": "4000"
            },
            read_timeout_seconds=60
        )
        return McpWorkbench(server_params=excel_server_params)


    # https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem
    @staticmethod
    def get_filesystem_workbench():
        fs_server_params = StdioServerParams(
            command="npx", args=[ "--yes", "@modelcontextprotocol/server-filesystem", "C:\\Users\\hp\\Downloads" ],
            read_timeout_seconds=60
        )
        return McpWorkbench(server_params=fs_server_params)