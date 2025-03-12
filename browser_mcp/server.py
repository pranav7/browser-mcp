from langchain_openai import ChatOpenAI
from mcp.server.fastmcp import FastMCP
from browser_use import Agent
from dotenv import load_dotenv
import logging
from typing import Literal
import os


# Create a null handler that suppresses all output
class NullHandler(logging.Handler):
    def emit(self, record):
        pass


# Configure root logger to suppress all output
root_logger = logging.getLogger()
root_logger.addHandler(NullHandler())
root_logger.setLevel(logging.CRITICAL)  # Only show critical errors

# Configure our app's logging to go to file
app_logger = logging.getLogger("browser-mcp")

# Create logs directory if it doesn't exist
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "browser-mcp.log")

file_handler = logging.FileHandler(log_file, mode="a")
file_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(name)s] [%(levelname)s] %(message)s")
)
app_logger.addHandler(file_handler)
app_logger.setLevel(logging.INFO)

# Suppress Playwright's logging
os.environ["PLAYWRIGHT_BROWSER_PATH"] = ""  # Suppress browser download messages
os.environ["PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD"] = "1"  # Skip automatic downloads
os.environ["DEBUG"] = ""  # Disable debug logging
os.environ["PWDEBUG"] = "0"  # Disable debug mode

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
        save_conversation_path="logs/conversation",
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
        save_conversation_path="logs/conversation",
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
        """
        mcp.run(transport=transport)
