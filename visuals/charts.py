"""
Chart generation for PEA ETF Tracker.

Provides Plotly chart creation functions for portfolio visualization.
"""

import logging
from datetime import date
from pathlib import Path
from typing import Dict, List

import plotly.express as px
import plotly.graph_objects as go

from config.settings import ChartPreferences

logger = logging.getLogger(__name__)

# Color schemes
COLOR_SCHEMES: Dict[str, List[str]] = {
    "plotly": px.colors.qualitative.Plotly,
    "pastel": px.colors.qualitative.Pastel,
    "bold": px.colors.qualitative.Bold,
}


def create_portfolio_value_chart(
    dates: List[date],
    values: List[float],
    title: str = "Portfolio Value Over Time",
) -> go.Figure:
    """
    Create line chart showing portfolio value over time.

    Args:
        dates: List of dates for x-axis.
        values: List of portfolio values for y-axis (in EUR).
        title: Chart title (default: "Portfolio Value Over Time").

    Returns:
        Plotly Figure object ready for display or export.

    Raises:
        ValueError: If dates and values have different lengths or are empty.

    Example:
        >>> from datetime import date
        >>> dates = [date(2024, 1, 1), date(2024, 1, 2)]
        >>> values = [10000.0, 10500.0]
        >>> fig = create_portfolio_value_chart(dates, values)
        >>> fig.show()  # doctest: +SKIP
    """
    if not dates or not values:
        raise ValueError("Dates and values cannot be empty")

    if len(dates) != len(values):
        raise ValueError(
            f"Dates ({len(dates)}) and values ({len(values)}) must have same length"
        )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=dates,
            y=values,
            mode="lines+markers",
            name="Portfolio Value",
            line={"color": "#1f77b4", "width": 2},
            marker={"size": 6},
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Value (EUR)",
        hovermode="x unified",
        template="plotly_white",
    )

    logger.info(f"Created portfolio value chart with {len(dates)} data points")
    return fig


def create_allocation_pie_chart(
    tickers: List[str],
    percentages: List[float],
    title: str = "Portfolio Allocation",
) -> go.Figure:
    """
    Create pie chart showing position allocation percentages.

    Args:
        tickers: List of ticker symbols.
        percentages: List of allocation percentages (0-100).
        title: Chart title (default: "Portfolio Allocation").

    Returns:
        Plotly Figure object ready for display or export.

    Raises:
        ValueError: If tickers and percentages have different lengths or are empty.

    Example:
        >>> tickers = ["EWLD.PA", "PE500.PA"]
        >>> percentages = [60.0, 40.0]
        >>> fig = create_allocation_pie_chart(tickers, percentages)
        >>> fig.show()  # doctest: +SKIP
    """
    if not tickers or not percentages:
        raise ValueError("Tickers and percentages cannot be empty")

    if len(tickers) != len(percentages):
        raise ValueError(
            f"Tickers ({len(tickers)}) and percentages ({len(percentages)}) "
            f"must have same length"
        )

    fig = go.Figure()

    fig.add_trace(
        go.Pie(
            labels=tickers,
            values=percentages,
            textinfo="label+percent",
            hovertemplate=(
                "<b>%{label}</b><br>%{percent}<br>%{value:.2f}%<extra></extra>"
            ),
        )
    )

    fig.update_layout(title=title, template="plotly_white")

    logger.info(f"Created allocation pie chart with {len(tickers)} positions")
    return fig


def create_allocation_bar_chart(
    tickers: List[str],
    values: List[float],
    title: str = "Position Values",
) -> go.Figure:
    """
    Create bar chart showing position values by ticker.

    Args:
        tickers: List of ticker symbols.
        values: List of position values (in EUR).
        title: Chart title (default: "Position Values").

    Returns:
        Plotly Figure object ready for display or export.

    Raises:
        ValueError: If tickers and values have different lengths or are empty.

    Example:
        >>> tickers = ["EWLD.PA", "PE500.PA"]
        >>> values = [6000.0, 4000.0]
        >>> fig = create_allocation_bar_chart(tickers, values)
        >>> fig.show()  # doctest: +SKIP
    """
    if not tickers or not values:
        raise ValueError("Tickers and values cannot be empty")

    if len(tickers) != len(values):
        raise ValueError(
            f"Tickers ({len(tickers)}) and values ({len(values)}) "
            f"must have same length"
        )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=tickers,
            y=values,
            name="Position Value",
            marker={"color": "#1f77b4"},
            hovertemplate="<b>%{x}</b><br>€%{y:.2f}<extra></extra>",
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title="Ticker",
        yaxis_title="Value (EUR)",
        template="plotly_white",
    )

    logger.info(f"Created allocation bar chart with {len(tickers)} positions")
    return fig


def create_risk_return_scatter(
    tickers: List[str],
    returns: List[float],
    volatilities: List[float],
    title: str = "Risk vs Return",
) -> go.Figure:
    """
    Create scatter plot of ETF returns vs volatility.

    Args:
        tickers: List of ticker symbols.
        returns: List of annualized returns (as decimals, e.g., 0.15 = 15%).
        volatilities: List of annualized volatilities (as decimals).
        title: Chart title (default: "Risk vs Return").

    Returns:
        Plotly Figure object ready for display or export.

    Raises:
        ValueError: If inputs have different lengths or are empty.

    Example:
        >>> tickers = ["EWLD.PA", "PE500.PA"]
        >>> returns = [0.12, 0.15]
        >>> volatilities = [0.18, 0.22]
        >>> fig = create_risk_return_scatter(tickers, returns, volatilities)
        >>> fig.show()  # doctest: +SKIP
    """
    if not tickers or not returns or not volatilities:
        raise ValueError("Tickers, returns, and volatilities cannot be empty")

    if len(tickers) != len(returns) or len(tickers) != len(volatilities):
        raise ValueError(
            f"Tickers ({len(tickers)}), returns ({len(returns)}), "
            f"and volatilities ({len(volatilities)}) must have same length"
        )

    # Convert to percentages for display
    returns_pct = [r * 100 for r in returns]
    volatilities_pct = [v * 100 for v in volatilities]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=volatilities_pct,
            y=returns_pct,
            mode="markers+text",
            text=tickers,
            textposition="top center",
            marker={"size": 12, "color": "#1f77b4"},
            hovertemplate="<b>%{text}</b><br>"
            "Return: %{y:.2f}%<br>"
            "Volatility: %{x:.2f}%<extra></extra>",
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title="Volatility (%)",
        yaxis_title="Return (%)",
        template="plotly_white",
    )

    logger.info(f"Created risk-return scatter with {len(tickers)} ETFs")
    return fig


def create_performance_chart(
    dates: List[date],
    prices: List[float],
    ticker: str,
    chart_type: str = "line",
) -> go.Figure:
    """
    Create line or candlestick chart for historical ETF performance.

    Args:
        dates: List of dates for x-axis.
        prices: List of closing prices for y-axis.
        ticker: Ticker symbol for chart title.
        chart_type: Chart type - "line" or "candlestick" (default: "line").

    Returns:
        Plotly Figure object ready for display or export.

    Raises:
        ValueError: If dates and prices have different lengths, are empty,
            or chart_type is invalid.

    Example:
        >>> from datetime import date
        >>> dates = [date(2024, 1, 1), date(2024, 1, 2)]
        >>> prices = [28.5, 29.0]
        >>> fig = create_performance_chart(dates, prices, "EWLD.PA")
        >>> fig.show()  # doctest: +SKIP
    """
    if not dates or not prices:
        raise ValueError("Dates and prices cannot be empty")

    if len(dates) != len(prices):
        raise ValueError(
            f"Dates ({len(dates)}) and prices ({len(prices)}) must have same length"
        )

    if chart_type not in ["line", "candlestick"]:
        raise ValueError(
            f"Invalid chart_type: {chart_type}. Use 'line' or 'candlestick'"
        )

    fig = go.Figure()

    if chart_type == "line":
        fig.add_trace(
            go.Scatter(
                x=dates,
                y=prices,
                mode="lines",
                name=ticker,
                line={"color": "#1f77b4", "width": 2},
                hovertemplate="<b>%{x}</b><br>€%{y:.2f}<extra></extra>",
            )
        )
    else:
        # For candlestick, we only have close prices, so create simple candlestick
        # with open=close (would need OHLC data for proper candlestick)
        logger.warning(
            "Candlestick chart requires OHLC data. Using line chart instead."
        )
        fig.add_trace(
            go.Scatter(
                x=dates,
                y=prices,
                mode="lines",
                name=ticker,
                line={"color": "#1f77b4", "width": 2},
                hovertemplate="<b>%{x}</b><br>€%{y:.2f}<extra></extra>",
            )
        )

    fig.update_layout(
        title=f"{ticker} Performance",
        xaxis_title="Date",
        yaxis_title="Price (EUR)",
        hovermode="x unified",
        template="plotly_white",
    )

    logger.info(f"Created performance chart for {ticker} with {len(dates)} data points")
    return fig


def apply_chart_theme(
    fig: go.Figure,
    preferences: ChartPreferences,
) -> go.Figure:
    """
    Apply user chart preferences to figure.

    Modifies the figure layout based on user preferences for grid, legend,
    and color scheme.

    Args:
        fig: Plotly Figure object to modify.
        preferences: ChartPreferences with user settings.

    Returns:
        Modified Plotly Figure object.

    Example:
        >>> from config.settings import ChartPreferences
        >>> prefs = ChartPreferences("portfolio_value", "plotly", True, True)
        >>> fig = go.Figure()
        >>> fig = apply_chart_theme(fig, prefs)
    """
    # Apply grid settings
    fig.update_xaxes(showgrid=preferences.show_grid)
    fig.update_yaxes(showgrid=preferences.show_grid)

    # Apply legend settings
    fig.update_layout(showlegend=preferences.show_legend)

    # Apply color scheme if available
    if preferences.color_scheme in COLOR_SCHEMES:
        colors = COLOR_SCHEMES[preferences.color_scheme]
        # Update trace colors if traces exist
        for i, trace in enumerate(fig.data):
            if hasattr(trace, "marker"):
                # Pie charts use 'colors' (plural), other charts use 'color'
                if hasattr(trace.marker, "colors"):
                    # Don't override pie chart colors - they're set automatically
                    pass
                elif hasattr(trace.marker, "color"):
                    trace.marker.color = colors[i % len(colors)]

    logger.debug(f"Applied chart theme: {preferences.color_scheme}")
    return fig


def export_chart_to_png(fig: go.Figure, path: Path) -> None:
    """
    Export chart to PNG file.

    Args:
        fig: Plotly Figure object to export.
        path: Path to save PNG file.

    Raises:
        OSError: If unable to write file.

    Example:
        >>> from pathlib import Path
        >>> fig = go.Figure()
        >>> export_chart_to_png(fig, Path("chart.png"))  # doctest: +SKIP
    """
    try:
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        # Export to PNG (requires kaleido package)
        fig.write_image(str(path))

        logger.info(f"Chart exported to PNG: {path}")

    except Exception as e:
        logger.error(f"Error exporting chart to PNG: {e}")
        raise OSError(f"Unable to export chart to {path}: {e}") from e


def export_chart_to_html(fig: go.Figure, path: Path) -> None:
    """
    Export chart to interactive HTML file.

    Args:
        fig: Plotly Figure object to export.
        path: Path to save HTML file.

    Raises:
        OSError: If unable to write file.

    Example:
        >>> from pathlib import Path
        >>> fig = go.Figure()
        >>> export_chart_to_html(fig, Path("chart.html"))  # doctest: +SKIP
    """
    try:
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        # Export to HTML
        with open(path, "w", encoding="utf-8") as f:
            f.write(fig.to_html())

        logger.info(f"Chart exported to HTML: {path}")

    except OSError as e:
        logger.error(f"Error exporting chart to HTML: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error exporting chart: {e}")
        raise OSError(f"Unable to export chart to {path}: {e}") from e
