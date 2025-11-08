"""
Tests for data.market_data module.

Tests market data fetching and caching functionality.
"""

from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pandas as pd
import pytest

from data.market_data import (
    fetch_historical_data,
    fetch_price,
    get_cached_price,
    load_price_cache,
    save_price_cache,
    update_price_cache,
)


# Cache tests
def test_load_price_cache_creates_directory_if_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """load_price_cache() creates cache directory if missing."""
    cache_dir = tmp_path / "cache_test"
    cache_file = cache_dir / "prices.json"

    monkeypatch.setattr("data.market_data.CACHE_DIR", cache_dir)
    monkeypatch.setattr("data.market_data.CACHE_FILE", cache_file)

    prices = load_price_cache()

    assert cache_dir.exists()
    assert isinstance(prices, dict)


def test_load_price_cache_returns_empty_dict_when_file_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """load_price_cache() returns {} when cache file doesn't exist."""
    cache_dir = tmp_path / "cache_test"
    cache_file = cache_dir / "prices.json"

    monkeypatch.setattr("data.market_data.CACHE_DIR", cache_dir)
    monkeypatch.setattr("data.market_data.CACHE_FILE", cache_file)

    prices = load_price_cache()

    assert prices == {}


def test_save_and_load_price_cache_preserves_data(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Prices saved and loaded are identical."""
    cache_dir = tmp_path / "cache_test"
    cache_file = cache_dir / "prices.json"

    monkeypatch.setattr("data.market_data.CACHE_DIR", cache_dir)
    monkeypatch.setattr("data.market_data.CACHE_FILE", cache_file)

    test_prices = {
        "EWLD.PA": 29.35,
        "PE500.PA": 43.12,
    }
    save_price_cache(test_prices)

    loaded_prices = load_price_cache()

    assert loaded_prices == test_prices


def test_update_price_cache_adds_new_ticker(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """update_price_cache() adds new ticker to cache."""
    cache_dir = tmp_path / "cache_test"
    cache_file = cache_dir / "prices.json"

    monkeypatch.setattr("data.market_data.CACHE_DIR", cache_dir)
    monkeypatch.setattr("data.market_data.CACHE_FILE", cache_file)

    update_price_cache("EWLD.PA", 29.35)

    prices = load_price_cache()
    assert "EWLD.PA" in prices
    assert prices["EWLD.PA"] == 29.35


def test_update_price_cache_updates_existing_ticker(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """update_price_cache() updates existing ticker price."""
    cache_dir = tmp_path / "cache_test"
    cache_file = cache_dir / "prices.json"

    monkeypatch.setattr("data.market_data.CACHE_DIR", cache_dir)
    monkeypatch.setattr("data.market_data.CACHE_FILE", cache_file)

    # Add initial price
    update_price_cache("EWLD.PA", 29.35)

    # Update price
    update_price_cache("EWLD.PA", 30.00)

    prices = load_price_cache()
    assert prices["EWLD.PA"] == 30.00


def test_get_cached_price_returns_price(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """get_cached_price() returns cached price if available."""
    cache_dir = tmp_path / "cache_test"
    cache_file = cache_dir / "prices.json"

    monkeypatch.setattr("data.market_data.CACHE_DIR", cache_dir)
    monkeypatch.setattr("data.market_data.CACHE_FILE", cache_file)

    save_price_cache({"EWLD.PA": 29.35})

    price = get_cached_price("EWLD.PA")

    assert price == 29.35


def test_get_cached_price_returns_none_when_not_found(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """get_cached_price() returns None when ticker not in cache."""
    cache_dir = tmp_path / "cache_test"
    cache_file = cache_dir / "prices.json"

    monkeypatch.setattr("data.market_data.CACHE_DIR", cache_dir)
    monkeypatch.setattr("data.market_data.CACHE_FILE", cache_file)

    price = get_cached_price("NONEXISTENT.PA")

    assert price is None


# fetch_price tests (with mocking)
@patch("data.market_data.yf.Ticker")
def test_fetch_price_returns_current_price(mock_ticker: Mock) -> None:
    """fetch_price() returns current price from Yahoo Finance."""
    mock_instance = MagicMock()
    mock_instance.info = {"currentPrice": 29.35}
    mock_ticker.return_value = mock_instance

    price = fetch_price("EWLD.PA", use_cache=False)

    assert price == 29.35
    mock_ticker.assert_called_once_with("EWLD.PA")


@patch("data.market_data.yf.Ticker")
def test_fetch_price_returns_regular_market_price(mock_ticker: Mock) -> None:
    """fetch_price() returns regularMarketPrice if currentPrice not available."""
    mock_instance = MagicMock()
    mock_instance.info = {"regularMarketPrice": 43.12}
    mock_ticker.return_value = mock_instance

    price = fetch_price("PE500.PA", use_cache=False)

    assert price == 43.12


@patch("data.market_data.yf.Ticker")
def test_fetch_price_handles_network_error_with_cache(
    mock_ticker: Mock, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """fetch_price() falls back to cache on network error."""
    cache_dir = tmp_path / "cache_test"
    cache_file = cache_dir / "prices.json"

    monkeypatch.setattr("data.market_data.CACHE_DIR", cache_dir)
    monkeypatch.setattr("data.market_data.CACHE_FILE", cache_file)

    # Set up cache
    save_price_cache({"EWLD.PA": 28.50})

    # Mock network error
    mock_ticker.side_effect = Exception("Network error")

    price = fetch_price("EWLD.PA", use_cache=True)

    assert price == 28.50


@patch("data.market_data.yf.Ticker")
def test_fetch_price_returns_none_when_no_cache(mock_ticker: Mock) -> None:
    """fetch_price() returns None when fetch fails and no cache."""
    mock_ticker.side_effect = Exception("Network error")

    price = fetch_price("EWLD.PA", use_cache=False)

    assert price is None


@patch("data.market_data.yf.Ticker")
def test_fetch_price_returns_none_when_no_price_data(mock_ticker: Mock) -> None:
    """fetch_price() returns None when no price data available."""
    mock_instance = MagicMock()
    mock_instance.info = {}
    mock_ticker.return_value = mock_instance

    price = fetch_price("EWLD.PA", use_cache=False)

    assert price is None


# fetch_historical_data tests
@patch("data.market_data.yf.Ticker")
def test_fetch_historical_data_returns_dataframe(mock_ticker: Mock) -> None:
    """fetch_historical_data() returns DataFrame with OHLCV data."""
    mock_instance = MagicMock()
    mock_df = pd.DataFrame(
        {
            "Open": [28.0, 28.5],
            "High": [28.8, 29.0],
            "Low": [27.5, 28.2],
            "Close": [28.5, 28.9],
            "Volume": [1000, 1100],
        }
    )
    mock_instance.history.return_value = mock_df
    mock_ticker.return_value = mock_instance

    df = fetch_historical_data("EWLD.PA", period="1mo")

    assert not df.empty
    assert len(df) == 2
    assert "Close" in df.columns
    mock_instance.history.assert_called_once_with(period="1mo")


@patch("data.market_data.yf.Ticker")
def test_fetch_historical_data_handles_error(mock_ticker: Mock) -> None:
    """fetch_historical_data() returns empty DataFrame on error."""
    mock_ticker.side_effect = Exception("Network error")

    df = fetch_historical_data("EWLD.PA")

    assert df.empty


@patch("data.market_data.yf.Ticker")
def test_fetch_historical_data_handles_empty_response(mock_ticker: Mock) -> None:
    """fetch_historical_data() returns empty DataFrame when no data available."""
    mock_instance = MagicMock()
    mock_instance.history.return_value = pd.DataFrame()
    mock_ticker.return_value = mock_instance

    df = fetch_historical_data("EWLD.PA")

    assert df.empty


@pytest.mark.parametrize(
    "period",
    ["1d", "5d", "1mo", "3mo", "1y"],
)
@patch("data.market_data.yf.Ticker")
def test_fetch_historical_data_supports_different_periods(
    mock_ticker: Mock, period: str
) -> None:
    """fetch_historical_data() supports different time periods."""
    mock_instance = MagicMock()
    mock_df = pd.DataFrame({"Close": [28.5]})
    mock_instance.history.return_value = mock_df
    mock_ticker.return_value = mock_instance

    df = fetch_historical_data("EWLD.PA", period=period)

    assert not df.empty
    mock_instance.history.assert_called_once_with(period=period)
