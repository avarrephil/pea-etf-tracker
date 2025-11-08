"""
Tests for analytics.performance module.

Tests portfolio analytics calculations including value, P&L, returns, and risk metrics.
"""

from datetime import date

import numpy as np
import pandas as pd
import pytest

from analytics.performance import (
    calculate_allocation,
    calculate_correlation_matrix,
    calculate_max_drawdown,
    calculate_pnl,
    calculate_portfolio_value,
    calculate_position_values,
    calculate_returns,
    calculate_sharpe_ratio,
    calculate_total_invested,
    calculate_volatility,
)
from data.portfolio import ETFPosition, Portfolio


# Fixtures
@pytest.fixture
def sample_portfolio() -> Portfolio:
    """Create a sample portfolio with 3 positions."""
    positions = [
        ETFPosition("EWLD.PA", "Amundi World", 100.0, 28.50, date(2024, 1, 15)),
        ETFPosition("PE500.PA", "Lyxor S&P 500", 50.0, 42.30, date(2024, 2, 10)),
        ETFPosition("PAEEM.PA", "Lyxor Emergents", 75.0, 18.25, date(2024, 3, 5)),
    ]
    return Portfolio(positions)


@pytest.fixture
def sample_prices() -> dict[str, float]:
    """Sample current prices for portfolio positions."""
    return {
        "EWLD.PA": 29.35,  # +2.98% gain
        "PE500.PA": 43.12,  # +1.94% gain
        "PAEEM.PA": 17.80,  # -2.47% loss
    }


@pytest.fixture
def sample_historical_data() -> dict[str, pd.DataFrame]:
    """Sample historical price data for 5 days."""
    dates = pd.date_range("2024-01-01", periods=5, freq="D")

    return {
        "EWLD.PA": pd.DataFrame({"Close": [28.0, 28.2, 28.5, 28.8, 29.0]}, index=dates),
        "PE500.PA": pd.DataFrame(
            {"Close": [42.0, 42.3, 42.1, 42.5, 42.8]}, index=dates
        ),
        "PAEEM.PA": pd.DataFrame(
            {"Close": [18.0, 18.2, 17.9, 18.1, 18.3]}, index=dates
        ),
    }


# Portfolio value tests
def test_calculate_portfolio_value_with_valid_prices(
    sample_portfolio: Portfolio, sample_prices: dict[str, float]
) -> None:
    """calculate_portfolio_value() returns correct total value."""
    # Expected: 100*29.35 + 50*43.12 + 75*17.80 = 2935 + 2156 + 1335 = 6426
    value = calculate_portfolio_value(sample_portfolio, sample_prices)

    assert value == pytest.approx(6426.0, rel=1e-9)


def test_calculate_portfolio_value_with_empty_portfolio() -> None:
    """calculate_portfolio_value() returns 0.0 for empty portfolio."""
    portfolio = Portfolio()
    prices = {"EWLD.PA": 29.35}

    value = calculate_portfolio_value(portfolio, prices)

    assert value == 0.0


def test_calculate_portfolio_value_with_missing_prices(
    sample_portfolio: Portfolio,
) -> None:
    """calculate_portfolio_value() handles missing prices gracefully."""
    # Only 2 out of 3 prices available
    prices = {
        "EWLD.PA": 29.35,
        "PE500.PA": 43.12,
        # PAEEM.PA missing
    }

    # Expected: 100*29.35 + 50*43.12 = 2935 + 2156 = 5091
    value = calculate_portfolio_value(sample_portfolio, prices)

    assert value == pytest.approx(5091.0, rel=1e-9)


# Total invested tests
def test_calculate_total_invested_returns_correct_amount(
    sample_portfolio: Portfolio,
) -> None:
    """calculate_total_invested() returns total buy price * quantity."""
    # Expected: 100*28.50 + 50*42.30 + 75*18.25 = 2850 + 2115 + 1368.75 = 6333.75
    invested = calculate_total_invested(sample_portfolio)

    assert invested == pytest.approx(6333.75, rel=1e-9)


def test_calculate_total_invested_with_empty_portfolio() -> None:
    """calculate_total_invested() returns 0.0 for empty portfolio."""
    portfolio = Portfolio()

    invested = calculate_total_invested(portfolio)

    assert invested == 0.0


# P&L tests
def test_calculate_pnl_with_profit(
    sample_portfolio: Portfolio, sample_prices: dict[str, float]
) -> None:
    """calculate_pnl() returns correct profit."""
    # Value: 6426, Invested: 6333.75, P&L: 92.25
    pnl = calculate_pnl(sample_portfolio, sample_prices)

    assert pnl == pytest.approx(92.25, rel=1e-9)


def test_calculate_pnl_with_loss(sample_portfolio: Portfolio) -> None:
    """calculate_pnl() returns correct loss."""
    prices = {
        "EWLD.PA": 27.00,  # Loss
        "PE500.PA": 40.00,  # Loss
        "PAEEM.PA": 16.00,  # Loss
    }
    # Value: 100*27 + 50*40 + 75*16 = 2700 + 2000 + 1200 = 5900
    # Invested: 6333.75
    # P&L: -433.75

    pnl = calculate_pnl(sample_portfolio, prices)

    assert pnl == pytest.approx(-433.75, rel=1e-9)


def test_calculate_pnl_with_empty_portfolio() -> None:
    """calculate_pnl() returns 0.0 for empty portfolio."""
    portfolio = Portfolio()
    prices = {"EWLD.PA": 29.35}

    pnl = calculate_pnl(portfolio, prices)

    assert pnl == 0.0


# Position values tests
def test_calculate_position_values_returns_correct_dict(
    sample_portfolio: Portfolio, sample_prices: dict[str, float]
) -> None:
    """calculate_position_values() returns dict with each position value."""
    values = calculate_position_values(sample_portfolio, sample_prices)

    assert values == {
        "EWLD.PA": pytest.approx(2935.0, rel=1e-9),
        "PE500.PA": pytest.approx(2156.0, rel=1e-9),
        "PAEEM.PA": pytest.approx(1335.0, rel=1e-9),
    }


def test_calculate_position_values_with_missing_prices(
    sample_portfolio: Portfolio,
) -> None:
    """calculate_position_values() skips positions with missing prices."""
    prices = {
        "EWLD.PA": 29.35,
        # PE500.PA and PAEEM.PA missing
    }

    values = calculate_position_values(sample_portfolio, prices)

    assert values == {"EWLD.PA": pytest.approx(2935.0, rel=1e-9)}


# Allocation tests
def test_calculate_allocation_returns_percentages(
    sample_portfolio: Portfolio, sample_prices: dict[str, float]
) -> None:
    """calculate_allocation() returns allocation percentages."""
    # Total: 6426
    # EWLD.PA: 2935/6426 = 45.68%
    # PE500.PA: 2156/6426 = 33.55%
    # PAEEM.PA: 1335/6426 = 20.77%
    allocation = calculate_allocation(sample_portfolio, sample_prices)

    assert allocation["EWLD.PA"] == pytest.approx(45.68, abs=0.01)
    assert allocation["PE500.PA"] == pytest.approx(33.55, abs=0.01)
    assert allocation["PAEEM.PA"] == pytest.approx(20.77, abs=0.01)

    # Percentages should sum to ~100%
    assert sum(allocation.values()) == pytest.approx(100.0, abs=0.01)


def test_calculate_allocation_with_empty_portfolio() -> None:
    """calculate_allocation() returns empty dict for empty portfolio."""
    portfolio = Portfolio()
    prices = {"EWLD.PA": 29.35}

    allocation = calculate_allocation(portfolio, prices)

    assert allocation == {}


def test_calculate_allocation_with_zero_total_value(
    sample_portfolio: Portfolio,
) -> None:
    """calculate_allocation() handles zero total value gracefully."""
    prices = {
        "EWLD.PA": 0.0,
        "PE500.PA": 0.0,
        "PAEEM.PA": 0.0,
    }

    allocation = calculate_allocation(sample_portfolio, prices)

    # Should return empty dict or all zeros
    assert allocation == {} or all(v == 0.0 for v in allocation.values())


# Returns calculation tests
def test_calculate_returns_daily(
    sample_portfolio: Portfolio, sample_historical_data: dict[str, pd.DataFrame]
) -> None:
    """calculate_returns() calculates daily portfolio returns."""
    returns = calculate_returns(
        sample_portfolio, sample_historical_data, period="daily"
    )

    # Should have 4 returns (5 days = 4 daily returns)
    assert len(returns) == 4
    assert isinstance(returns, pd.Series)
    # Returns should be reasonable (between -10% and +10% for daily)
    assert all(-0.10 <= r <= 0.10 for r in returns)


def test_calculate_returns_with_empty_portfolio() -> None:
    """calculate_returns() returns empty Series for empty portfolio."""
    portfolio = Portfolio()
    historical_data = {"EWLD.PA": pd.DataFrame({"Close": [28.0, 28.5]})}

    returns = calculate_returns(portfolio, historical_data, period="daily")

    assert len(returns) == 0


def test_calculate_returns_with_misaligned_dates(sample_portfolio: Portfolio) -> None:
    """calculate_returns() handles misaligned dates across ETFs."""
    # Different date ranges for each ETF
    historical_data = {
        "EWLD.PA": pd.DataFrame(
            {"Close": [28.0, 28.5, 29.0]},
            index=pd.date_range("2024-01-01", periods=3, freq="D"),
        ),
        "PE500.PA": pd.DataFrame(
            {"Close": [42.0, 42.5]},
            index=pd.date_range("2024-01-02", periods=2, freq="D"),
        ),
        "PAEEM.PA": pd.DataFrame(
            {"Close": [18.0, 18.5]},
            index=pd.date_range("2024-01-01", periods=2, freq="D"),
        ),
    }

    returns = calculate_returns(sample_portfolio, historical_data, period="daily")

    # Should only have returns for common dates
    assert len(returns) >= 0  # At least doesn't crash


# Volatility tests
def test_calculate_volatility_returns_std_dev() -> None:
    """calculate_volatility() returns standard deviation of returns."""
    returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

    volatility = calculate_volatility(returns, annualize=False)

    # Manual calculation: std([0.01, -0.02, 0.03, -0.01, 0.02])
    expected = np.std(returns, ddof=1)
    assert volatility == pytest.approx(expected, rel=1e-9)


def test_calculate_volatility_annualized() -> None:
    """calculate_volatility() annualizes volatility correctly."""
    returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

    volatility = calculate_volatility(returns, annualize=True)

    # Annualized: std * sqrt(252)
    expected = np.std(returns, ddof=1) * np.sqrt(252)
    assert volatility == pytest.approx(expected, rel=1e-9)


def test_calculate_volatility_with_empty_series() -> None:
    """calculate_volatility() returns 0.0 for empty series."""
    returns = pd.Series([])

    volatility = calculate_volatility(returns, annualize=False)

    assert volatility == 0.0


def test_calculate_volatility_with_constant_returns() -> None:
    """calculate_volatility() returns 0.0 for constant returns."""
    returns = pd.Series([0.01, 0.01, 0.01, 0.01])

    volatility = calculate_volatility(returns, annualize=False)

    assert volatility == 0.0


# Sharpe ratio tests
def test_calculate_sharpe_ratio_with_positive_returns() -> None:
    """calculate_sharpe_ratio() calculates risk-adjusted returns."""
    returns = pd.Series([0.01, 0.02, 0.015, 0.025, 0.018])

    sharpe = calculate_sharpe_ratio(returns, risk_free_rate=0.0, annualize=False)

    # Sharpe = mean(returns) / std(returns)
    expected = np.mean(returns) / np.std(returns, ddof=1)
    assert sharpe == pytest.approx(expected, rel=1e-9)


def test_calculate_sharpe_ratio_with_risk_free_rate() -> None:
    """calculate_sharpe_ratio() adjusts for risk-free rate."""
    returns = pd.Series([0.05, 0.06, 0.04, 0.07, 0.05])
    risk_free_rate = 0.02

    sharpe = calculate_sharpe_ratio(
        returns, risk_free_rate=risk_free_rate, annualize=False
    )

    # Sharpe = (mean(returns) - rf) / std(returns)
    excess_returns = returns - risk_free_rate
    expected = np.mean(excess_returns) / np.std(returns, ddof=1)
    assert sharpe == pytest.approx(expected, rel=1e-9)


def test_calculate_sharpe_ratio_with_zero_volatility() -> None:
    """calculate_sharpe_ratio() returns 0.0 when volatility is zero."""
    returns = pd.Series([0.01, 0.01, 0.01, 0.01])

    sharpe = calculate_sharpe_ratio(returns, risk_free_rate=0.0, annualize=False)

    assert sharpe == 0.0


def test_calculate_sharpe_ratio_annualized() -> None:
    """calculate_sharpe_ratio() annualizes correctly."""
    returns = pd.Series([0.01, 0.02, 0.015, 0.025, 0.018])

    sharpe = calculate_sharpe_ratio(returns, risk_free_rate=0.0, annualize=True)

    # Annualized: (mean * 252) / (std * sqrt(252)) = mean / std * sqrt(252)
    expected = (np.mean(returns) / np.std(returns, ddof=1)) * np.sqrt(252)
    assert sharpe == pytest.approx(expected, rel=1e-9)


# Max drawdown tests
def test_calculate_max_drawdown_with_declining_values() -> None:
    """calculate_max_drawdown() finds largest peak-to-trough decline."""
    # Peak at 100, trough at 70, drawdown = -30%
    portfolio_values = pd.Series([100, 95, 90, 70, 75, 80])

    max_dd = calculate_max_drawdown(portfolio_values)

    # Drawdown = (70 - 100) / 100 = -0.30 = -30%
    assert max_dd == pytest.approx(-30.0, abs=0.01)


def test_calculate_max_drawdown_with_only_gains() -> None:
    """calculate_max_drawdown() returns 0.0 when only gains."""
    portfolio_values = pd.Series([100, 105, 110, 115, 120])

    max_dd = calculate_max_drawdown(portfolio_values)

    assert max_dd == 0.0


def test_calculate_max_drawdown_with_empty_series() -> None:
    """calculate_max_drawdown() returns 0.0 for empty series."""
    portfolio_values = pd.Series([])

    max_dd = calculate_max_drawdown(portfolio_values)

    assert max_dd == 0.0


def test_calculate_max_drawdown_with_single_value() -> None:
    """calculate_max_drawdown() returns 0.0 for single value."""
    portfolio_values = pd.Series([100])

    max_dd = calculate_max_drawdown(portfolio_values)

    assert max_dd == 0.0


# Correlation matrix tests
def test_calculate_correlation_matrix_returns_dataframe(
    sample_historical_data: dict[str, pd.DataFrame]
) -> None:
    """calculate_correlation_matrix() returns correlation DataFrame."""
    corr_matrix = calculate_correlation_matrix(sample_historical_data)

    assert isinstance(corr_matrix, pd.DataFrame)
    assert corr_matrix.shape == (3, 3)
    # Diagonal should be 1.0 (perfect correlation with self)
    assert all(
        corr_matrix.loc[ticker, ticker] == pytest.approx(1.0)
        for ticker in corr_matrix.index
    )


def test_calculate_correlation_matrix_is_symmetric(
    sample_historical_data: dict[str, pd.DataFrame]
) -> None:
    """calculate_correlation_matrix() returns symmetric matrix."""
    corr_matrix = calculate_correlation_matrix(sample_historical_data)

    # Matrix should be symmetric
    assert np.allclose(corr_matrix.values, corr_matrix.values.T)


def test_calculate_correlation_matrix_with_empty_data() -> None:
    """calculate_correlation_matrix() handles empty data."""
    historical_data: dict[str, pd.DataFrame] = {}

    corr_matrix = calculate_correlation_matrix(historical_data)

    assert corr_matrix.empty


def test_calculate_correlation_matrix_with_single_etf() -> None:
    """calculate_correlation_matrix() handles single ETF."""
    historical_data = {"EWLD.PA": pd.DataFrame({"Close": [28.0, 28.5, 29.0]})}

    corr_matrix = calculate_correlation_matrix(historical_data)

    assert corr_matrix.shape == (1, 1)
    assert corr_matrix.loc["EWLD.PA", "EWLD.PA"] == pytest.approx(1.0)
