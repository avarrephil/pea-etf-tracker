"""
PEA ETF Tracker - Main Application Entry Point.

This module initializes the PyQt6 application, loads user settings,
and launches the main window.

Usage:
    python main.py
"""

import sys
import logging
from pathlib import Path
from typing import NoReturn

# Configure logging
LOG_DIR = Path.home() / "Library/Logs/PEA_ETF_Tracker"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)


def main() -> NoReturn:
    """
    Main application entry point.

    Initializes the PyQt6 application, loads user settings and last portfolio,
    creates the main window, and starts the event loop.

    Exits:
        System exit code from QApplication.exec()
    """
    logger.info("Starting PEA ETF Tracker v1.0.0")

    try:
        # Import PyQt6 here to handle import errors gracefully
        from PyQt6.QtWidgets import QApplication

        # Create application instance
        app = QApplication(sys.argv)
        app.setApplicationName("PEA ETF Tracker")
        app.setOrganizationName("Philippe Avarre")
        app.setApplicationVersion("1.0.0")

        logger.info("Application initialized successfully")

        # TODO: Load user settings from config module
        # TODO: Load last opened portfolio
        # TODO: Create and show main window
        # TODO: Set up signal handlers

        # For Phase 1, just show a placeholder message
        logger.info("Phase 1: Foundation complete - UI implementation pending")
        logger.info(
            "Application structure ready. Phase 2 will implement core data models."
        )

        # TODO: Replace with actual main window in Phase 5
        # main_window = MainWindow()
        # main_window.show()

        logger.info("Application ready. Exiting Phase 1 stub.")
        sys.exit(0)

    except ImportError as e:
        logger.error(f"Failed to import required modules: {e}")
        logger.error("Please install dependencies: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error during application startup: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
