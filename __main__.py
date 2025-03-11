#!/usr/bin/env python3
"""
Entry point for the browser-mcp package.
This allows the package to be run directly with `uvx browser-mcp`.
"""

from server import mcp


def main():
    """Main entry point for the application when run via uvx."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
