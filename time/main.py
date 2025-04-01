import datetime
from typing import Dict

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("time_service")

@mcp.tool(description="現在時刻を取得")
def get_current_time() -> Dict:
    dt_now = datetime.datetime.now()
    result = dt_now.strftime('%Y年%m月%d日 %H:%M:%S')
    return {
        "time": result
    }

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')