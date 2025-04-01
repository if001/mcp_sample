import datetime
from typing import Dict

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("echo_service")

@mcp.tool(description="天照を起動する")
def do_amaterasu() -> Dict:
    result = "🔥🔥🔥天照🔥🔥🔥"
    return {
        "value": result
    }

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')