import datetime
from typing import Dict

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("echo_service")

@mcp.tool(description="天照を起動する")
def do_amaterasu() -> Dict:
    result = """
:rinnegan_sasuke: :mangekyou_sasuke_eien:                                    人人人人人人人人
     :くちびる:                                   ＞　          :amaterasu:         　＜
                                              ￣Y^Y^Y^Y^Y^Y^Y￣
:火::火::火:
    """
    return {
        "value": result
    }

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')