from typing import Dict

import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("search_web_service")

@mcp.tool(description="webを検索する")
def web_scrape(self, url: str) -> Dict:
    """
    Scrape and process a web page using r.jina.ai

    :param url: The URL of the web page to scrape.
    :return: The scraped and processed content without the Links/Buttons section, or an error message.
    """
    jina_url = f"https://r.jina.ai/{url}"

    headers = {
        "X-No-Cache": "true",
        "X-With-Images-Summary": "true",
        "X-With-Links-Summary": "true",
    }

    try:
        response = requests.get(jina_url, headers=headers)
        response.raise_for_status()

        # Extract content and remove Links/Buttons section as its too many tokens
        content = response.text
        links_section_start = content.rfind("Images:")
        if links_section_start != -1:
            content = content[:links_section_start].strip()

        return {
            "content": content
        }
    except requests.RequestException as e:
        return {
            "content": f"Error scraping web page: {str(e)}"
        }


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')