"""
Market data fetching and caching for PEA ETF Tracker.

Fetches ETF prices from Yahoo Finance with local caching for offline support.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Optional

import pandas as pd
import yfinance as yf

logger = logging.getLogger(__name__)

CACHE_DIR = Path.home() / "Library/Application Support/PEA_ETF_Tracker/cache"
CACHE_FILE = CACHE_DIR / "prices.json"


def load_price_cache() -> Dict[str, float]:
    """
    Load cached prices from file.

    Returns:
        Dictionary mapping ticker to price. Empty dict if file doesn't exist.

    Example:
        >>> prices = load_price_cache()
        >>> print(prices.get("EWLD.PA"))
        29.35
    """
    try:
        # Ensure cache directory exists
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

        if not CACHE_FILE.exists():
            logger.debug("Cache file does not exist, returning empty cache")
            return {}

        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache_data = json.load(f)

        # Return prices dictionary
        if isinstance(cache_data, dict) and "prices" in cache_data:
            prices_dict = cache_data["prices"]
            if isinstance(prices_dict, dict):
                return prices_dict

        # Legacy format: just a dict of prices
        if isinstance(cache_data, dict):
            return dict(cache_data)

        return {}

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in cache file: {e}")
        return {}
    except Exception as e:
        logger.error(f"Error loading price cache: {e}")
        return {}


def save_price_cache(prices: Dict[str, float]) -> None:
    """
    Save prices to cache file.

    Args:
        prices: Dictionary mapping ticker to price.

    Example:
        >>> save_price_cache({"EWLD.PA": 29.35})
    """
    try:
        # Ensure cache directory exists
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

        # Save with timestamp for future use
        cache_data = {
            "prices": prices,
        }

        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, indent=2)

        logger.debug(f"Price cache saved with {len(prices)} tickers")

    except Exception as e:
        logger.error(f"Error saving price cache: {e}")


def get_cached_price(ticker: str) -> Optional[float]:
    """
    Get cached price for ticker.

    Args:
        ticker: Ticker symbol.

    Returns:
        Cached price or None if not found.

    Example:
        >>> price = get_cached_price("EWLD.PA")
    """
    prices = load_price_cache()
    return prices.get(ticker)


def update_price_cache(ticker: str, price: float) -> None:
    """
    Update cache with new price.

    Args:
        ticker: Ticker symbol.
        price: Current price.

    Example:
        >>> update_price_cache("EWLD.PA", 29.35)
    """
    prices = load_price_cache()
    prices[ticker] = price
    save_price_cache(prices)


def fetch_price(ticker: str, use_cache: bool = True) -> Optional[float]:
    """
    Fetch current price for ticker from Yahoo Finance.

    Falls back to cached price if network request fails and use_cache=True.

    Args:
        ticker: Ticker symbol (e.g., "EWLD.PA").
        use_cache: If True, return cached price on network failure.

    Returns:
        Current price in EUR or None if unavailable.

    Example:
        >>> price = fetch_price("EWLD.PA")
        >>> if price:
        ...     print(f"Price: {price} EUR")
    """
    try:
        etf = yf.Ticker(ticker)
        info = etf.info

        # Try to get current price from various fields
        price = info.get("currentPrice") or info.get("regularMarketPrice")

        if price:
            logger.info(f"Fetched price for {ticker}: {price} EUR")
            update_price_cache(ticker, float(price))
            return float(price)

        logger.warning(f"No price data available for {ticker}")
        if use_cache:
            cached = get_cached_price(ticker)
            if cached:
                logger.info(f"Using cached price for {ticker}: {cached} EUR")
                return cached
        return None

    except Exception as e:
        logger.error(f"Error fetching price for {ticker}: {e}")
        if use_cache:
            cached = get_cached_price(ticker)
            if cached:
                logger.info(
                    f"Using cached price for {ticker} after error: {cached} EUR"
                )
                return cached
        return None


def fetch_historical_data(ticker: str, period: str = "1mo") -> pd.DataFrame:
    """
    Fetch historical price data for ticker.

    Args:
        ticker: Ticker symbol (e.g., "EWLD.PA").
        period: Time period (e.g., "1d", "5d", "1mo", "3mo", "1y").

    Returns:
        DataFrame with columns: Date, Open, High, Low, Close, Volume.
        Empty DataFrame if fetch fails.

    Example:
        >>> df = fetch_historical_data("EWLD.PA", period="1y")
        >>> if not df.empty:
        ...     print(f"Fetched {len(df)} days of data")
    """
    try:
        etf = yf.Ticker(ticker)
        hist: pd.DataFrame = etf.history(period=period)

        if hist.empty:
            logger.warning(f"No historical data available for {ticker}")
            return pd.DataFrame()

        logger.info(f"Fetched {len(hist)} days of data for {ticker}")
        return hist

    except Exception as e:
        logger.error(f"Error fetching historical data for {ticker}: {e}")
        return pd.DataFrame()
