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
async def search_web(task: str, model: str = "gpt-4o-mini") -> str:
    """Search the web for information relevant to the task.
    Use this tool for basic web searches.

    Args:
        task: The task to complete.
        model: The OpenAI model to use for the LLM (default: gpt-4o-mini)
    """
    agent = Agent(
        task=task,
        llm=ChatOpenAI(model=model),
    )
    history = await agent.run()
    return (
        history.final_result()
        or "The task was completed but the result is not available."
    )


@mcp.tool()
async def search_web_with_planning(
    task: str, base_model: str = "gpt-4o-mini", planning_model: str = "o3-mini"
) -> str:
    """Search the web for information relevant to the task.
    Use this tool for complex web searches that require planning.

    Args:
        task: The task to complete.
        base_model: The OpenAI model to use for the base LLM (default: gpt-4o-mini)
        planning_model: The OpenAI model to use for the planning LLM (default: o3-mini)
    """
    agent = Agent(
        task=task,
        llm=ChatOpenAI(model=base_model),
        planner_llm=ChatOpenAI(model=planning_model),
        planner_interval=10,
    )
    history = await agent.run()
    return (
        history.final_result()
        or "The task was completed but the result is not available."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
else:

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
