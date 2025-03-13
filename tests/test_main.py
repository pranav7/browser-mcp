"""
Tests for the main function in browser_mcp/__main__.py
"""

import unittest
from unittest.mock import patch, MagicMock, call
import sys


class MainFunctionTest(unittest.TestCase):
    """Test the main function in browser_mcp/__main__.py"""

    @patch("browser_mcp.__main__.check_playwright_installed")
    @patch("browser_mcp.__main__.install_playwright_browsers")
    @patch("browser_mcp.__main__.mcp.run")
    @patch("browser_mcp.__main__.app_logger")
    def test_main_with_playwright_installed(
        self, mock_logger, mock_mcp_run, mock_install, mock_check_installed
    ):
        """Test that main function works when Playwright is already installed"""
        # Configure mocks
        mock_check_installed.return_value = True

        # Import the main function (after patching)
        from browser_mcp.__main__ import main

        # Call the main function
        main()

        # Verify the expected behavior
        mock_check_installed.assert_called_once()
        mock_install.assert_not_called()  # Should not try to install if already installed
        mock_mcp_run.assert_called_once_with(transport="stdio")

    @patch("browser_mcp.__main__.check_playwright_installed")
    @patch("browser_mcp.__main__.install_playwright_browsers")
    @patch("browser_mcp.__main__.mcp.run")
    @patch("browser_mcp.__main__.app_logger")
    def test_main_with_successful_installation(
        self, mock_logger, mock_mcp_run, mock_install, mock_check_installed
    ):
        """Test that main function works when Playwright needs to be installed"""
        # Configure mocks to simulate successful installation
        mock_check_installed.side_effect = [
            False,
            True,
        ]  # First False, then True after install
        mock_install.return_value = True

        # Import the main function (after patching)
        from browser_mcp.__main__ import main

        # Call the main function
        main()

        # Verify the expected behavior
        mock_logger.info.assert_any_call("Attempting to install Playwright browsers...")
        mock_check_installed.assert_called()
        self.assertEqual(
            mock_check_installed.call_count, 2
        )  # Called before and after install
        mock_install.assert_called_once()
        mock_mcp_run.assert_called_once_with(transport="stdio")

    @patch("browser_mcp.__main__.check_playwright_installed")
    @patch("browser_mcp.__main__.install_playwright_browsers")
    @patch("browser_mcp.__main__.mcp.run")
    @patch("browser_mcp.__main__.app_logger")
    @patch("browser_mcp.__main__.sys.exit")
    def test_main_with_failed_installation(
        self,
        mock_exit,
        mock_logger,
        mock_mcp_run,
        mock_install,
        mock_check_installed,
    ):
        """Test that main function exits when Playwright installation fails"""
        # Configure mocks to simulate failed installation
        # The check_playwright_installed is called twice in the implementation
        # First to check if it's installed, then to verify after installation attempt
        mock_check_installed.side_effect = [False, False]
        mock_install.return_value = False

        # Import the main function (after patching)
        from browser_mcp.__main__ import main

        # Call the main function
        main()

        # Verify the expected behavior
        mock_logger.info.assert_any_call("Attempting to install Playwright browsers...")
        self.assertEqual(
            mock_check_installed.call_count, 2
        )  # Called twice in the implementation
        mock_install.assert_called_once()
        mock_logger.error.assert_any_call(
            "Failed to install playwright browsers. Please run 'playwright install' manually."
        )
        # sys.exit is called twice in the implementation
        self.assertEqual(mock_exit.call_count, 2)
        self.assertEqual(mock_exit.call_args_list, [call(1), call(1)])
        # Since sys.exit is mocked, the code continues execution and calls mcp.run
        mock_mcp_run.assert_called_once_with(transport="stdio")

    @patch("browser_mcp.__main__.check_playwright_installed")
    @patch("browser_mcp.__main__.install_playwright_browsers")
    @patch("browser_mcp.__main__.mcp.run")
    @patch("browser_mcp.__main__.app_logger")
    @patch("browser_mcp.__main__.sys.exit")
    def test_main_with_verification_failure(
        self,
        mock_exit,
        mock_logger,
        mock_mcp_run,
        mock_install,
        mock_check_installed,
    ):
        """Test that main function exits when Playwright verification fails after installation"""
        # Configure mocks to simulate successful installation but failed verification
        mock_check_installed.side_effect = [
            False,
            False,
        ]  # False before and after install
        mock_install.return_value = True

        # Import the main function (after patching)
        from browser_mcp.__main__ import main

        # Call the main function
        main()

        # Verify the expected behavior
        mock_logger.info.assert_any_call("Attempting to install Playwright browsers...")
        self.assertEqual(
            mock_check_installed.call_count, 2
        )  # Called before and after install
        mock_install.assert_called_once()
        mock_logger.error.assert_called_with(
            "Playwright browsers installation verification failed. Please check your installation."
        )
        mock_exit.assert_called_once_with(1)
        # Since sys.exit is mocked, the code continues execution and calls mcp.run
        mock_mcp_run.assert_called_once_with(transport="stdio")


if __name__ == "__main__":
    # This allows running the tests directly with python
    unittest.main()
