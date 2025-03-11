# browser-use-mcp

A MCP (Model Control Protocol) server for [browser-use](https://github.com/browser-use/browser-use) library.

## Setup

```bash
# Install dependencies
pip install -e .
```

## Usage

```bash
# Run the MCP server
python main.py
```

## Available RPC Methods

- `browse(url)` - Navigate to a URL
- `screenshot()` - Take a screenshot of the current page
- `get_html()` - Get the HTML content of the current page

## Example

```python
from mcp.client import Client

async def main():
    client = await Client.connect()
    
    # Navigate to a URL
    await client.rpc("browse", url="https://example.com")
    
    # Get HTML content
    result = await client.rpc("get_html")
    print(result["html"])
    
    # Take a screenshot
    screenshot = await client.rpc("screenshot")
    # Use the screenshot data
    
    await client.close()
```