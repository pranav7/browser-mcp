from langchain_openai import ChatOpenAI
from mcp.server.fastmcp import FastMCP
from browser_use import Agent
from dotenv import load_dotenv
import logging
from typing import Literal

# Get the configured logger from the main module
app_logger = logging.getLogger("browser-mcp")

# Load environment variables
load_dotenv()

# Configure the MCP server
mcp = FastMCP("browser-use")


@mcp.tool()
async def search_web(task: str, model: str = "gpt-4o-mini") -> str:
    """Search the web for information relevant to the task.
    Use this tool for basic web searches.

    Args:
        task: The task to complete.
        model: The OpenAI model to use for the LLM (default: gpt-4o-mini)
    """
    app_logger.info(f"Starting web search task: {task}")
    agent = Agent(
        task=task,
        llm=ChatOpenAI(model=model),
        save_conversation_path="logs/conversation",
    )
    history = await agent.run()
    result = (
        history.final_result()
        or "The task was completed but the result is not available."
    )
    app_logger.info("Completed web search task")
    return result


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
    app_logger.info(f"Starting web search with planning task: {task}")
    agent = Agent(
        task=task,
        llm=ChatOpenAI(model=base_model),
        planner_llm=ChatOpenAI(model=planning_model),
        planner_interval=10,
        save_conversation_path="logs/conversation",
    )
    history = await agent.run()
    result = (
        history.final_result()
        or "The task was completed but the result is not available."
    )
    app_logger.info("Completed web search with planning task")
    return result


if __name__ == "__main__":
    app_logger.info("Running MCP server directly...")
    mcp.run(transport="stdio")
else:

    def run(
        transport: Literal["stdio", "sse"] = "stdio",
    ):
        """
        Run the MCP server with the specified transport.
        This function is called when the package is imported via uvx.
        """
        app_logger.info(f"Starting MCP server with {transport} transport...")
        mcp.run(transport=transport)
