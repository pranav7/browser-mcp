"""
Main entry point for browser-mcp that checks dependencies before starting the server
"""

import subprocess
import sys
import logging

from browser_mcp.server import run as server_run, mcp
from browser_mcp.check_playwright import check_playwright_browsers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] [%(levelname)s] %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("browser-mcp")


def check_playwright_installed():
    """
    Check if playwright and its browsers are installed by attempting to launch a browser.
    This is more reliable than checking command line tools.
    """
    success, browsers = check_playwright_browsers()
    if success:
        logger.info(f"Playwright is installed with browsers: {', '.join(browsers)}")
    return success


def install_playwright_browsers():
    """Install Chromium browser using the Python API"""
    logger.info("Installing Chromium browser...")
    try:
        from playwright.sync_api import sync_playwright
        import sys
        import subprocess

        # Install only Chromium browser
        subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"], check=True
        )

        # Verify installation by attempting to create a playwright instance
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch()
                browser.close()
            except Exception as e:
                logger.error(f"Failed to verify Chromium installation: {e}")
                return False

        logger.info("Chromium browser installed and verified successfully.")
        return True
    except Exception as e:
        logger.error(f"Error installing Chromium browser: {e}")
        return False


def create_app():
    """
    Create and configure the FastAPI application.
    This is the function that uvicorn will import and use.
    """
    # Ensure dependencies are installed when creating the app
    if not check_playwright_installed():
        install_playwright_browsers()
        if not check_playwright_installed():
            logger.error("Failed to install required dependencies.")
            sys.exit(1)

    return mcp


def main():
    """
    Main entry point for browser-mcp.
    This is used when running the package directly.
    """
    # Check if playwright is installed with browsers
    if not check_playwright_installed():
        logger.info("Attempting to install Playwright browsers...")
        if not install_playwright_browsers():
            logger.error(
                "Failed to install playwright browsers. Please run 'playwright install' manually."
            )
            sys.exit(1)

        # Verify installation was successful
        if not check_playwright_installed():
            logger.error(
                "Playwright browsers installation verification failed. Please check your installation."
            )
            sys.exit(1)

    # Run the server
    server_run()


# This allows both direct execution and uvicorn to work
app = create_app()

if __name__ == "__main__":
    main()
