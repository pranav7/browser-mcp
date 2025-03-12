import asyncio
from server import search_web, search_web_with_planning
from dotenv import load_dotenv

load_dotenv()


async def test():
    # Simple task to test browser functionality
    result = await search_web("What is the main headline on the New York Times today?")
    print(f"Result: {result}")

    result = await search_web_with_planning(
        "How far is mars from earth in kilometers?",
        base_model="gpt-4o-mini",
        planning_model="o3-mini",
    )
    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(test())
