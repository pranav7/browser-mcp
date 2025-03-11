# browser-mcp

A MCP (Model Control Protocol) server for [browser-use](https://github.com/browser-use/browser-use) library. This package allows AI agents to perform web browsing tasks through a standardized interface.

## Installation

You can install the package using pip:

```bash
pip install browser-mcp
```

Or with uv (recommended):

```bash
uv pip install browser-mcp
```

## Setup

For development, clone the repository and install in development mode:

```bash
# Clone the repository
git clone https://github.com/pranav7/browser-mcp.git
cd browser-mcp

# Install dependencies with uv
uv pip install -e .

# Or with pip
pip install -e .
```

## Environment Variables

Create a `.env` file with your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

## Usage

### Running the MCP Server

You can run the MCP server directly with Python:

```bash
python -m browser_mcp
```

Or if you have uv installed:

```bash
uvx browser-mcp
```

### Using as a Client

```python
from mcp.client import Client

async def main():
    client = await Client.connect()

    # Perform a task with the browser
    result = await client.rpc("perform_task_with_browser",
                             task="Search for the latest news about AI and summarize the top 3 results")
    print(result)

    await client.close()
```

## Available RPC Methods

- `perform_task_with_browser(task: str)` - Performs a specified task using the browser-use Agent with GPT-4o-mini

## Development

### Testing

Tests can be run with:

```bash
python -m unittest discover
```

### Publishing to PyPI

This project uses GitHub Actions to automatically publish to PyPI when a new release is created. The workflow:

1. Builds the package using uv
2. Publishes it to PyPI using trusted publishing

To create a new release:

1. Update the version in `pyproject.toml`
2. Create a new release on GitHub
3. The GitHub Action will automatically build and publish the package

## License

[MIT License](LICENSE)