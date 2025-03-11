from langchain_openai import ChatOpenAI
from mcp.server.fastmcp import FastMCP
from browser_use import Agent
from dotenv import load_dotenv
import logging
import sys
from typing import Literal

# Configure logging to go to stderr instead of stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] [%(levelname)s] %(message)s",
    stream=sys.stderr,
)

load_dotenv()

mcp = FastMCP("browser-use")


@mcp.tool()
async def perform_task_with_browser(task: str) -> str:
    agent = Agent(
        task=task,
        llm=ChatOpenAI(model="gpt-4o-mini"),
    )
    history = await agent.run()
    return (
        history.final_result()
        or "The task was completed but the result is not available."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
else:
    # When imported as a module (e.g., via uvx), this function will be called
    def run(
        transport: Literal["stdio", "sse"] = "stdio",
    ):
        """
        Run the MCP server with the specified transport.
        This function is called when the package is imported via uvx.

        Args:
            transport: The transport to use for communication. Either "stdio" or "sse".
        """
        mcp.run(transport=transport)
