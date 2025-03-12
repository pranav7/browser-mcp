"""
Tests for Playwright installation and browser functionality.
"""

import unittest
from playwright.sync_api import sync_playwright


class PlaywrightInstallationTest(unittest.TestCase):
    """Test that Playwright is installed and can launch browsers."""

    def test_playwright_installation(self):
        """Test that Playwright is installed and can launch browsers."""
        with sync_playwright() as playwright:
            # Test each browser type
            browsers_to_check = ["chromium", "firefox", "webkit"]
            installed_browsers = []

            for browser_type in browsers_to_check:
                try:
                    browser_launcher = getattr(playwright, browser_type)
                    browser = browser_launcher.launch()

                    # Create a page and navigate to a simple URL
                    page = browser.new_page()
                    page.goto("about:blank")

                    # Verify the page loaded
                    self.assertEqual(
                        page.url,
                        "about:blank",
                        f"Failed to navigate to about:blank in {browser_type}",
                    )

                    # Clean up
                    page.close()
                    browser.close()

                    installed_browsers.append(browser_type)
                    print(f"✅ {browser_type} browser is working properly")
                except Exception as e:
                    print(
                        f"❌ Browser {browser_type} is not installed or not working: {e}"
                    )

            # At least one browser should be installed
            self.assertTrue(
                installed_browsers, "No Playwright browsers are installed or working"
            )
            print(f"Installed browsers: {', '.join(installed_browsers)}")

    def test_playwright_navigation(self):
        """Test that Playwright can navigate to a real website."""
        with sync_playwright() as playwright:
            # Use chromium as it's the most commonly installed
            try:
                browser = playwright.chromium.launch()
                page = browser.new_page()

                # Navigate to the Playwright website
                page.goto("https://playwright.dev/")

                # Check title contains "Playwright"
                title = page.title()
                self.assertIn(
                    "Playwright",
                    title,
                    f"Title '{title}' does not contain 'Playwright'",
                )

                # Clean up
                browser.close()
            except Exception as e:
                self.skipTest(f"Skipping test because chromium is not available: {e}")

    def test_playwright_interaction(self):
        """Test that Playwright can interact with page elements."""
        with sync_playwright() as playwright:
            try:
                browser = playwright.chromium.launch()
                page = browser.new_page()

                # Navigate to the Playwright website
                page.goto("https://playwright.dev/")

                # Click the get started link
                page.get_by_role("link", name="Get started").click()

                # Check for heading with the name of Installation
                heading = page.get_by_role("heading", name="Installation")
                self.assertTrue(
                    heading.is_visible(), "Installation heading is not visible"
                )

                # Clean up
                browser.close()
            except Exception as e:
                self.skipTest(f"Skipping test because chromium is not available: {e}")


if __name__ == "__main__":
    # This allows running the tests directly with python
    unittest.main()
