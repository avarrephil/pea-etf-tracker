"""
Performance analytics for PEA ETF Tracker.

Provides portfolio value, returns, P&L, allocation, and risk calculations.
"""

import logging
from typing import Dict

import numpy as np
import pandas as pd

from data.portfolio import Portfolio

logger = logging.getLogger(__name__)

# Annual trading days for annualization
ANNUAL_TRADING_DAYS = 252


def calculate_portfolio_value(portfolio: Portfolio, prices: Dict[str, float]) -> float:
    """
    Calculate total portfolio value in EUR.

    Args:
        portfolio: Portfolio object with positions.
        prices: Dictionary mapping ticker to current price in EUR.

    Returns:
        Total portfolio value (sum of position values). Returns 0.0 if portfolio
        is empty or all prices are missing.

    Example:
        >>> portfolio = Portfolio([
        ...     ETFPosition("EWLD.PA", "Amundi World", 100, 28.50, date.today())
        ... ])
        >>> prices = {"EWLD.PA": 29.35}
        >>> calculate_portfolio_value(portfolio, prices)
        2935.0
    """
    total_value = 0.0

    for position in portfolio.get_all_positions():
        # Use manual price if set, otherwise use fetched price
        effective_price = None
        if position.manual_price is not None:
            effective_price = position.manual_price
        elif position.ticker in prices:
            effective_price = prices[position.ticker]

        if effective_price is not None:
            position_value = position.quantity * effective_price
            total_value += position_value
        else:
            logger.warning(f"Price not available for {position.ticker}, skipping")

    return total_value


def calculate_total_invested(portfolio: Portfolio) -> float:
    """
    Calculate total amount invested (buy_price × quantity).

    Args:
        portfolio: Portfolio object with positions.

    Returns:
        Total invested amount in EUR. Returns 0.0 if portfolio is empty.

    Example:
        >>> portfolio = Portfolio([
        ...     ETFPosition("EWLD.PA", "Amundi World", 100, 28.50, date.today())
        ... ])
        >>> calculate_total_invested(portfolio)
        2850.0
    """
    total_invested = 0.0

    for position in portfolio.get_all_positions():
        total_invested += position.quantity * position.buy_price

    return total_invested


def calculate_pnl(portfolio: Portfolio, prices: Dict[str, float]) -> float:
    """
    Calculate profit/loss (current value - invested).

    Args:
        portfolio: Portfolio object with positions.
        prices: Dictionary mapping ticker to current price in EUR.

    Returns:
        Total P&L in EUR. Positive for profit, negative for loss.
        Returns 0.0 if portfolio is empty.

    Example:
        >>> portfolio = Portfolio([
        ...     ETFPosition("EWLD.PA", "Amundi World", 100, 28.50, date.today())
        ... ])
        >>> prices = {"EWLD.PA": 29.35}
        >>> calculate_pnl(portfolio, prices)
        85.0
    """
    current_value = calculate_portfolio_value(portfolio, prices)
    invested = calculate_total_invested(portfolio)

    return current_value - invested


def calculate_position_values(
    portfolio: Portfolio, prices: Dict[str, float]
) -> Dict[str, float]:
    """
    Calculate value for each position.

    Args:
        portfolio: Portfolio object with positions.
        prices: Dictionary mapping ticker to current price in EUR.

    Returns:
        Dictionary mapping ticker to position value in EUR.
        Only includes positions with available prices.

    Example:
        >>> portfolio = Portfolio([
        ...     ETFPosition("EWLD.PA", "Amundi World", 100, 28.50, date.today()),
        ...     ETFPosition("PE500.PA", "Lyxor S&P 500", 50, 42.30, date.today())
        ... ])
        >>> prices = {"EWLD.PA": 29.35, "PE500.PA": 43.12}
        >>> calculate_position_values(portfolio, prices)
        {'EWLD.PA': 2935.0, 'PE500.PA': 2156.0}
    """
    position_values = {}

    for position in portfolio.get_all_positions():
        if position.ticker in prices:
            position_values[position.ticker] = (
                position.quantity * prices[position.ticker]
            )
        else:
            logger.warning(f"Price not available for {position.ticker}, skipping")

    return position_values


def calculate_allocation(
    portfolio: Portfolio, prices: Dict[str, float]
) -> Dict[str, float]:
    """
    Calculate allocation percentage for each position.

    Args:
        portfolio: Portfolio object with positions.
        prices: Dictionary mapping ticker to current price in EUR.

    Returns:
        Dictionary mapping ticker to allocation percentage (0-100).
        Returns empty dict if total value is zero or portfolio is empty.
        Percentages sum to 100.0.

    Example:
        >>> portfolio = Portfolio([
        ...     ETFPosition("EWLD.PA", "Amundi World", 100, 28.50, date.today()),
        ...     ETFPosition("PE500.PA", "Lyxor S&P 500", 50, 42.30, date.today())
        ... ])
        >>> prices = {"EWLD.PA": 29.35, "PE500.PA": 43.12}
        >>> allocations = calculate_allocation(portfolio, prices)
        >>> allocations["EWLD.PA"]  # doctest: +SKIP
        57.65
    """
    position_values = calculate_position_values(portfolio, prices)
    total_value = sum(position_values.values())

    if total_value == 0.0:
        logger.warning("Total portfolio value is zero, cannot calculate allocation")
        return {}

    allocations = {}
    for ticker, value in position_values.items():
        allocations[ticker] = (value / total_value) * 100.0

    return allocations


def calculate_returns(
    portfolio: Portfolio,
    historical_data: Dict[str, pd.DataFrame],
    period: str = "daily",
) -> pd.Series:
    """
    Calculate portfolio returns over time.

    Args:
        portfolio: Portfolio object with positions.
        historical_data: Dictionary mapping ticker to DataFrame with "Close" column.
        period: Return period - "daily", "weekly", or "monthly" (default: "daily").

    Returns:
        Series of portfolio returns indexed by date.
        Returns empty Series if portfolio is empty or no common dates.

    Example:
        >>> portfolio = Portfolio([
        ...     ETFPosition("EWLD.PA", "Amundi World", 100, 28.50, date.today())
        ... ])
        >>> historical_data = {
        ...     "EWLD.PA": pd.DataFrame({"Close": [28.0, 28.5, 29.0]})
        ... }
        >>> returns = calculate_returns(portfolio, historical_data)
        >>> len(returns)  # doctest: +SKIP
        2
    """
    if not portfolio.get_all_positions():
        logger.warning("Portfolio is empty, returning empty returns")
        return pd.Series(dtype=float)

    # Extract quantities for each ticker
    quantities = {}
    for position in portfolio.get_all_positions():
        if position.ticker in historical_data:
            quantities[position.ticker] = position.quantity
        else:
            logger.warning(
                f"Historical data not available for {position.ticker}, skipping"
            )

    if not quantities:
        logger.warning("No historical data for any positions")
        return pd.Series(dtype=float)

    # Combine historical prices for all positions
    price_dfs = []
    for ticker, df in historical_data.items():
        if ticker in quantities:
            if "Close" in df.columns:
                price_series = df["Close"].rename(ticker)
                price_dfs.append(price_series)

    if not price_dfs:
        return pd.Series(dtype=float)

    # Merge all price series on common dates (inner join)
    prices_df = pd.concat(price_dfs, axis=1, join="inner")

    if prices_df.empty:
        logger.warning("No common dates across historical data")
        return pd.Series(dtype=float)

    # Calculate portfolio value for each date
    portfolio_values = pd.Series(0.0, index=prices_df.index)
    for ticker in prices_df.columns:
        portfolio_values += prices_df[ticker] * quantities[ticker]

    # Calculate returns
    returns: pd.Series = portfolio_values.pct_change().dropna()

    # Resample if needed
    if period == "weekly":
        resampled = returns.resample("W").apply(lambda x: (1 + x).prod() - 1)
        returns = pd.Series(resampled) if isinstance(resampled, pd.Series) else returns
    elif period == "monthly":
        resampled = returns.resample("M").apply(lambda x: (1 + x).prod() - 1)
        returns = pd.Series(resampled) if isinstance(resampled, pd.Series) else returns
    # "daily" is default, no resampling needed

    return returns


def calculate_volatility(returns: pd.Series, annualize: bool = True) -> float:
    """
    Calculate volatility (standard deviation of returns).

    Args:
        returns: Series of portfolio returns.
        annualize: If True, annualize volatility using sqrt(252) (default: True).

    Returns:
        Volatility as decimal (e.g., 0.15 = 15%). Returns 0.0 if returns
        series is empty or has constant values.

    Example:
        >>> returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])
        >>> volatility = calculate_volatility(returns, annualize=False)
        >>> volatility  # doctest: +SKIP
        0.0187
    """
    if len(returns) == 0:
        logger.warning("Returns series is empty, returning 0.0 volatility")
        return 0.0

    volatility = float(returns.std(ddof=1))

    if np.isnan(volatility):
        return 0.0

    if annualize:
        volatility *= np.sqrt(ANNUAL_TRADING_DAYS)

    return volatility


def calculate_sharpe_ratio(
    returns: pd.Series, risk_free_rate: float = 0.0, annualize: bool = True
) -> float:
    """
    Calculate Sharpe ratio (risk-adjusted returns).

    Args:
        returns: Series of portfolio returns.
        risk_free_rate: Risk-free rate as decimal (default: 0.0).
        annualize: If True, annualize Sharpe ratio (default: True).

    Returns:
        Sharpe ratio. Returns 0.0 if volatility is zero or returns are empty.
        Higher values indicate better risk-adjusted returns.

    Example:
        >>> returns = pd.Series([0.01, 0.02, 0.015, 0.025, 0.018])
        >>> sharpe = calculate_sharpe_ratio(returns, risk_free_rate=0.0)
        >>> sharpe  # doctest: +SKIP
        1.85
    """
    if len(returns) == 0:
        logger.warning("Returns series is empty, returning 0.0 Sharpe ratio")
        return 0.0

    volatility = calculate_volatility(returns, annualize=False)

    if volatility == 0.0:
        logger.warning("Volatility is zero, returning 0.0 Sharpe ratio")
        return 0.0

    excess_returns = returns - risk_free_rate
    mean_excess_return = float(excess_returns.mean())

    sharpe = mean_excess_return / volatility

    if annualize:
        sharpe *= np.sqrt(ANNUAL_TRADING_DAYS)

    return sharpe


def calculate_max_drawdown(portfolio_values: pd.Series) -> float:
    """
    Calculate maximum drawdown (largest peak-to-trough decline).

    Args:
        portfolio_values: Series of portfolio values over time.

    Returns:
        Maximum drawdown as percentage (e.g., -30.0 for 30% decline).
        Returns 0.0 if values series is empty or only has gains.

    Example:
        >>> values = pd.Series([100, 95, 90, 70, 75, 80])
        >>> max_dd = calculate_max_drawdown(values)
        >>> max_dd  # doctest: +SKIP
        -30.0
    """
    if len(portfolio_values) == 0:
        logger.warning("Portfolio values series is empty, returning 0.0")
        return 0.0

    # Calculate running maximum
    running_max = portfolio_values.cummax()

    # Calculate drawdown at each point
    drawdown = (portfolio_values - running_max) / running_max * 100.0

    # Find maximum drawdown (most negative value)
    max_dd = float(drawdown.min())

    # If no drawdown occurred, return 0.0
    if max_dd > 0.0 or np.isnan(max_dd):
        return 0.0

    return max_dd


def calculate_correlation_matrix(
    historical_data: Dict[str, pd.DataFrame]
) -> pd.DataFrame:
    """
    Calculate correlation matrix between ETFs.

    Args:
        historical_data: Dictionary mapping ticker to DataFrame with "Close" column.

    Returns:
        DataFrame with correlation matrix (tickers as both index and columns).
        Returns empty DataFrame if historical_data is empty.
        Diagonal values are 1.0 (perfect correlation with self).

    Example:
        >>> historical_data = {
        ...     "EWLD.PA": pd.DataFrame({"Close": [28.0, 28.5, 29.0]}),
        ...     "PE500.PA": pd.DataFrame({"Close": [42.0, 42.5, 43.0]})
        ... }
        >>> corr = calculate_correlation_matrix(historical_data)
        >>> corr.loc["EWLD.PA", "EWLD.PA"]  # doctest: +SKIP
        1.0
    """
    if not historical_data:
        logger.warning("Historical data is empty, returning empty correlation matrix")
        return pd.DataFrame()

    # Extract Close prices for each ticker
    price_dfs = []
    for ticker, df in historical_data.items():
        if "Close" in df.columns:
            price_series = df["Close"].rename(ticker)
            price_dfs.append(price_series)
        else:
            logger.warning(f"No 'Close' column for {ticker}, skipping")

    if not price_dfs:
        return pd.DataFrame()

    # Merge all price series on common dates (inner join)
    prices_df = pd.concat(price_dfs, axis=1, join="inner")

    if prices_df.empty:
        logger.warning("No common dates across historical data")
        return pd.DataFrame()

    # Calculate returns
    returns_df = prices_df.pct_change().dropna()

    # Calculate correlation matrix
    corr_matrix = returns_df.corr()

    return corr_matrix
