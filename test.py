import asyncio
from server import perform_task_with_browser
from dotenv import load_dotenv

load_dotenv()


async def test():
    # Simple task to test browser functionality
    result = await perform_task_with_browser(
        "Go to example.com and tell me the title of the page"
    )
    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(test())
