"""
Configuration management for PEA ETF Tracker.

Handles loading, saving, and validation of user settings.
Settings are persisted to ~/Library/Application Support/PEA_ETF_Tracker/config.json
"""

import json
import logging
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

CONFIG_DIR = Path.home() / "Library/Application Support/PEA_ETF_Tracker"
CONFIG_FILE = CONFIG_DIR / "config.json"


@dataclass
class ChartPreferences:
    """Chart display preferences."""

    default_chart: str
    color_scheme: str
    show_grid: bool
    show_legend: bool


@dataclass
class WindowGeometry:
    """Main window geometry."""

    width: int
    height: int
    x: int
    y: int


@dataclass
class ETFInfo:
    """ETF information for default portfolio."""

    ticker: str
    name: str
    weight: float


@dataclass
class Settings:
    """Application settings."""

    default_currency: str
    data_source: str
    auto_refresh_enabled: bool
    auto_refresh_interval_minutes: int
    etfs: List[ETFInfo]
    chart_preferences: ChartPreferences
    last_portfolio_path: str
    window_geometry: WindowGeometry


def get_default_settings() -> Settings:
    """
    Get default application settings.

    Returns:
        Settings object with sensible defaults.

    Example:
        >>> settings = get_default_settings()
        >>> settings.default_currency
        'EUR'
    """
    return Settings(
        default_currency="EUR",
        data_source="yfinance",
        auto_refresh_enabled=False,
        auto_refresh_interval_minutes=5,
        etfs=[
            ETFInfo(
                ticker="EWLD.PA",
                name="Amundi MSCI World UCITS ETF",
                weight=0.30,
            ),
            ETFInfo(
                ticker="PE500.PA",
                name="Lyxor PEA S&P 500 UCITS ETF",
                weight=0.25,
            ),
            ETFInfo(
                ticker="PAEEM.PA",
                name="Lyxor PEA Emergents MSCI EM",
                weight=0.15,
            ),
            ETFInfo(
                ticker="PCEU.PA",
                name="Lyxor STOXX Europe 600 UCITS ETF",
                weight=0.20,
            ),
            ETFInfo(
                ticker="PSP5.PA",
                name="Amundi MSCI Europe UCITS ETF",
                weight=0.10,
            ),
        ],
        chart_preferences=ChartPreferences(
            default_chart="portfolio_value",
            color_scheme="plotly",
            show_grid=True,
            show_legend=True,
        ),
        last_portfolio_path="",
        window_geometry=WindowGeometry(
            width=1200,
            height=800,
            x=100,
            y=100,
        ),
    )


def _settings_to_dict(settings: Settings) -> Dict[str, Any]:
    """
    Convert Settings object to dictionary for JSON serialization.

    Args:
        settings: Settings object to convert.

    Returns:
        Dictionary representation of settings.
    """
    data = asdict(settings)
    return data


def _dict_to_settings(data: Dict[str, Any]) -> Settings:
    """
    Convert dictionary to Settings object.

    Args:
        data: Dictionary with settings data.

    Returns:
        Settings object.

    Raises:
        KeyError: If required keys are missing.
        TypeError: If data types are incorrect.
    """
    return Settings(
        default_currency=data["default_currency"],
        data_source=data["data_source"],
        auto_refresh_enabled=data["auto_refresh_enabled"],
        auto_refresh_interval_minutes=data["auto_refresh_interval_minutes"],
        etfs=[
            ETFInfo(
                ticker=etf["ticker"],
                name=etf["name"],
                weight=etf["weight"],
            )
            for etf in data["etfs"]
        ],
        chart_preferences=ChartPreferences(
            default_chart=data["chart_preferences"]["default_chart"],
            color_scheme=data["chart_preferences"]["color_scheme"],
            show_grid=data["chart_preferences"]["show_grid"],
            show_legend=data["chart_preferences"]["show_legend"],
        ),
        last_portfolio_path=data["last_portfolio_path"],
        window_geometry=WindowGeometry(
            width=data["window_geometry"]["width"],
            height=data["window_geometry"]["height"],
            x=data["window_geometry"]["x"],
            y=data["window_geometry"]["y"],
        ),
    )


def load_settings() -> Settings:
    """
    Load settings from config file.

    If config file doesn't exist or is corrupted, returns defaults.
    Creates config directory if it doesn't exist.

    Returns:
        Settings object loaded from file or defaults.

    Example:
        >>> settings = load_settings()
        >>> print(settings.default_currency)
        EUR
    """
    try:
        # Ensure config directory exists
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        # Check if config file exists
        if not CONFIG_FILE.exists():
            logger.info(f"Config file not found at {CONFIG_FILE}, using defaults")
            return get_default_settings()

        # Load and parse JSON
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Convert to Settings object
        settings = _dict_to_settings(data)
        logger.info(f"Settings loaded from {CONFIG_FILE}")
        return settings

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in config file: {e}")
        logger.info("Using default settings")
        return get_default_settings()
    except (KeyError, TypeError) as e:
        logger.error(f"Invalid config file format: {e}")
        logger.info("Using default settings")
        return get_default_settings()
    except Exception as e:
        logger.error(f"Error loading settings: {e}", exc_info=True)
        logger.info("Using default settings")
        return get_default_settings()


def save_settings(settings: Settings) -> None:
    """
    Save settings to config file.

    Creates config directory if it doesn't exist.

    Args:
        settings: Settings object to save.

    Raises:
        PermissionError: If unable to write to config directory.
        OSError: If unable to create directory or write file.

    Example:
        >>> settings = get_default_settings()
        >>> settings.default_currency = "USD"
        >>> save_settings(settings)
    """
    try:
        # Ensure config directory exists
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        # Convert to dictionary
        data = _settings_to_dict(settings)

        # Write to file
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        logger.info(f"Settings saved to {CONFIG_FILE}")

    except PermissionError as e:
        logger.error(f"Permission denied writing to {CONFIG_FILE}: {e}")
        raise
    except OSError as e:
        logger.error(f"Error writing settings to {CONFIG_FILE}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error saving settings: {e}", exc_info=True)
        raise
