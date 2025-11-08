"""
PEA ETF Tracker - Main Application Entry Point.

Initializes PyQt6 application, loads settings and portfolio, launches main window.
"""

import sys
import logging
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from config.settings import load_settings
from data.portfolio import Portfolio
from ui.main_window import MainWindow

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


def main() -> int:
    """
    Main application entry point.

    Loads settings and portfolio, creates main window, starts event loop.

    Returns:
        Exit code (0 for success, 1 for error).

    Example:
        >>> sys.exit(main())  # doctest: +SKIP
    """
    logger.info("Starting PEA ETF Tracker v1.0.0")

    try:
        # Load settings
        settings = load_settings()
        logger.info("Settings loaded successfully")

        # Load last portfolio or create empty
        portfolio = Portfolio()
        if settings.last_portfolio_path:
            try:
                portfolio = Portfolio.load_from_json(Path(settings.last_portfolio_path))
                logger.info(f"Loaded portfolio: {settings.last_portfolio_path}")
            except Exception as e:
                logger.warning(f"Could not load last portfolio: {e}")
                logger.info("Starting with empty portfolio")

        # Create Qt application
        app = QApplication(sys.argv)
        app.setApplicationName("PEA ETF Tracker")
        app.setOrganizationName("Philippe Avarre")
        app.setApplicationVersion("1.0.0")

        # Create and show main window
        window = MainWindow(settings, portfolio)
        window.show()

        logger.info("Application started successfully")
        return app.exec()

    except ImportError as e:
        logger.error(f"Failed to import required modules: {e}")
        logger.error("Please install dependencies: pip install -r requirements.txt")
        return 1
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
