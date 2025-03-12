"""
Utility script to check if Playwright and its browsers are properly installed.
This can be run independently to verify the installation.
"""

import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] [%(levelname)s] %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("browser-mcp-check")


def check_playwright_browsers():
    """
    Check if Playwright and its browsers are installed by attempting to launch each browser.
    Returns a tuple of (success, installed_browsers_list).
    """
    try:
        logger.info("Checking Playwright and browser installation...")

        # Import here to avoid dependency issues if not installed
        from playwright.sync_api import sync_playwright

        with sync_playwright() as playwright:
            # Try to launch each browser type
            browsers_to_check = ["chromium", "firefox", "webkit"]
            installed_browsers = []

            for browser_type in browsers_to_check:
                try:
                    logger.info(f"Testing {browser_type} browser...")
                    browser_launcher = getattr(playwright, browser_type)
                    browser = browser_launcher.launch()

                    # Create a page and navigate to a simple URL to verify functionality
                    page = browser.new_page()
                    page.goto("about:blank")

                    # Verify the page loaded correctly
                    if page.url != "about:blank":
                        logger.warning(
                            f"Browser {browser_type} failed to navigate to about:blank"
                        )
                        continue

                    # Clean up
                    page.close()
                    browser.close()

                    installed_browsers.append(browser_type)
                    logger.info(f"✅ {browser_type} browser is working properly")
                except Exception as e:
                    logger.warning(
                        f"❌ Browser {browser_type} is not installed or not working: {e}"
                    )

            if installed_browsers:
                logger.info(
                    f"Playwright is installed with browsers: {', '.join(installed_browsers)}"
                )
                return True, installed_browsers
            else:
                logger.error("No Playwright browsers are installed or working.")
                return False, []

    except ImportError:
        logger.error("Playwright package is not installed.")
        return False, []
    except Exception as e:
        logger.error(f"Error checking Playwright installation: {e}")
        return False, []


def main():
    """Run the Playwright check as a standalone script"""
    success, browsers = check_playwright_browsers()

    if success:
        logger.info("✅ Playwright check completed successfully")
        logger.info(f"Installed browsers: {', '.join(browsers)}")
        return 0
    else:
        logger.error("❌ Playwright check failed - no browsers are working")
        logger.error("Please run 'playwright install' to install the required browsers")
        return 1


if __name__ == "__main__":
    sys.exit(main())
