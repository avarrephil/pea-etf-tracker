"""
Tests for visuals.charts module.

Tests chart generation functions for portfolio visualization.
"""

from datetime import date
from pathlib import Path

import plotly.graph_objects as go
import pytest

from config.settings import ChartPreferences
from visuals.charts import (
    apply_chart_theme,
    create_allocation_bar_chart,
    create_allocation_pie_chart,
    create_performance_chart,
    create_portfolio_value_chart,
    create_risk_return_scatter,
    export_chart_to_html,
    export_chart_to_png,
)


# Fixtures
@pytest.fixture
def sample_dates() -> list[date]:
    """Sample dates for time series charts."""
    return [date(2024, 1, 1), date(2024, 1, 2), date(2024, 1, 3)]


@pytest.fixture
def sample_values() -> list[float]:
    """Sample portfolio values."""
    return [10000.0, 10500.0, 10200.0]


@pytest.fixture
def sample_tickers() -> list[str]:
    """Sample ticker symbols."""
    return ["EWLD.PA", "PE500.PA", "PAEEM.PA"]


@pytest.fixture
def sample_percentages() -> list[float]:
    """Sample allocation percentages."""
    return [45.0, 35.0, 20.0]


@pytest.fixture
def chart_preferences() -> ChartPreferences:
    """Sample chart preferences."""
    return ChartPreferences(
        default_chart="portfolio_value",
        color_scheme="plotly",
        show_grid=True,
        show_legend=True,
    )


# Portfolio value chart tests
def test_create_portfolio_value_chart_returns_figure(
    sample_dates: list[date], sample_values: list[float]
) -> None:
    """create_portfolio_value_chart() returns valid Plotly Figure."""
    fig = create_portfolio_value_chart(sample_dates, sample_values)

    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1
    assert fig.data[0].type == "scatter"


def test_create_portfolio_value_chart_has_correct_data(
    sample_dates: list[date], sample_values: list[float]
) -> None:
    """create_portfolio_value_chart() contains correct data points."""
    fig = create_portfolio_value_chart(sample_dates, sample_values)

    trace = fig.data[0]
    assert len(trace.x) == 3
    assert len(trace.y) == 3
    assert list(trace.y) == sample_values


def test_create_portfolio_value_chart_with_custom_title(
    sample_dates: list[date], sample_values: list[float]
) -> None:
    """create_portfolio_value_chart() accepts custom title."""
    title = "My Portfolio"
    fig = create_portfolio_value_chart(sample_dates, sample_values, title=title)

    assert fig.layout.title.text == title


def test_create_portfolio_value_chart_with_empty_data() -> None:
    """create_portfolio_value_chart() raises ValueError for empty data."""
    with pytest.raises(ValueError, match="cannot be empty"):
        create_portfolio_value_chart([], [])


def test_create_portfolio_value_chart_with_mismatched_lengths(
    sample_dates: list[date],
) -> None:
    """create_portfolio_value_chart() raises ValueError for mismatched lengths."""
    with pytest.raises(ValueError, match="must have same length"):
        create_portfolio_value_chart(sample_dates, [100.0, 200.0])


# Allocation pie chart tests
def test_create_allocation_pie_chart_returns_figure(
    sample_tickers: list[str], sample_percentages: list[float]
) -> None:
    """create_allocation_pie_chart() returns valid Plotly Figure."""
    fig = create_allocation_pie_chart(sample_tickers, sample_percentages)

    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1
    assert fig.data[0].type == "pie"


def test_create_allocation_pie_chart_has_correct_data(
    sample_tickers: list[str], sample_percentages: list[float]
) -> None:
    """create_allocation_pie_chart() contains correct labels and values."""
    fig = create_allocation_pie_chart(sample_tickers, sample_percentages)

    trace = fig.data[0]
    assert list(trace.labels) == sample_tickers
    assert list(trace.values) == sample_percentages


def test_create_allocation_pie_chart_with_empty_data() -> None:
    """create_allocation_pie_chart() raises ValueError for empty data."""
    with pytest.raises(ValueError, match="cannot be empty"):
        create_allocation_pie_chart([], [])


def test_create_allocation_pie_chart_with_mismatched_lengths(
    sample_tickers: list[str],
) -> None:
    """create_allocation_pie_chart() raises ValueError for mismatched lengths."""
    with pytest.raises(ValueError, match="must have same length"):
        create_allocation_pie_chart(sample_tickers, [50.0, 50.0])


# Allocation bar chart tests
def test_create_allocation_bar_chart_returns_figure(
    sample_tickers: list[str], sample_values: list[float]
) -> None:
    """create_allocation_bar_chart() returns valid Plotly Figure."""
    fig = create_allocation_bar_chart(sample_tickers, sample_values)

    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1
    assert fig.data[0].type == "bar"


def test_create_allocation_bar_chart_has_correct_data(
    sample_tickers: list[str], sample_values: list[float]
) -> None:
    """create_allocation_bar_chart() contains correct x and y data."""
    fig = create_allocation_bar_chart(sample_tickers, sample_values)

    trace = fig.data[0]
    assert list(trace.x) == sample_tickers
    assert list(trace.y) == sample_values


def test_create_allocation_bar_chart_with_empty_data() -> None:
    """create_allocation_bar_chart() raises ValueError for empty data."""
    with pytest.raises(ValueError, match="cannot be empty"):
        create_allocation_bar_chart([], [])


def test_create_allocation_bar_chart_with_mismatched_lengths(
    sample_tickers: list[str],
) -> None:
    """create_allocation_bar_chart() raises ValueError for mismatched lengths."""
    with pytest.raises(ValueError, match="must have same length"):
        create_allocation_bar_chart(sample_tickers, [1000.0])


# Risk-return scatter tests
def test_create_risk_return_scatter_returns_figure(
    sample_tickers: list[str],
) -> None:
    """create_risk_return_scatter() returns valid Plotly Figure."""
    returns = [0.12, 0.15, 0.10]
    volatilities = [0.18, 0.22, 0.15]

    fig = create_risk_return_scatter(sample_tickers, returns, volatilities)

    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1
    assert fig.data[0].type == "scatter"


def test_create_risk_return_scatter_converts_to_percentages(
    sample_tickers: list[str],
) -> None:
    """create_risk_return_scatter() converts decimals to percentages."""
    returns = [0.12, 0.15, 0.10]
    volatilities = [0.18, 0.22, 0.15]

    fig = create_risk_return_scatter(sample_tickers, returns, volatilities)

    trace = fig.data[0]
    # Returns converted to percentages
    assert list(trace.y) == [12.0, 15.0, 10.0]
    # Volatilities converted to percentages
    assert list(trace.x) == [18.0, 22.0, 15.0]


def test_create_risk_return_scatter_with_empty_data() -> None:
    """create_risk_return_scatter() raises ValueError for empty data."""
    with pytest.raises(ValueError, match="cannot be empty"):
        create_risk_return_scatter([], [], [])


def test_create_risk_return_scatter_with_mismatched_lengths(
    sample_tickers: list[str],
) -> None:
    """create_risk_return_scatter() raises ValueError for mismatched lengths."""
    with pytest.raises(ValueError, match="must have same length"):
        create_risk_return_scatter(sample_tickers, [0.1, 0.2], [0.15])


# Performance chart tests
def test_create_performance_chart_returns_figure(
    sample_dates: list[date], sample_values: list[float]
) -> None:
    """create_performance_chart() returns valid Plotly Figure."""
    fig = create_performance_chart(sample_dates, sample_values, "EWLD.PA")

    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1
    assert fig.data[0].type == "scatter"


def test_create_performance_chart_includes_ticker_in_title(
    sample_dates: list[date], sample_values: list[float]
) -> None:
    """create_performance_chart() includes ticker in title."""
    ticker = "EWLD.PA"
    fig = create_performance_chart(sample_dates, sample_values, ticker)

    assert ticker in fig.layout.title.text


def test_create_performance_chart_with_line_type(
    sample_dates: list[date], sample_values: list[float]
) -> None:
    """create_performance_chart() creates line chart."""
    fig = create_performance_chart(
        sample_dates, sample_values, "EWLD.PA", chart_type="line"
    )

    assert fig.data[0].type == "scatter"
    assert fig.data[0].mode == "lines"


def test_create_performance_chart_with_candlestick_type(
    sample_dates: list[date], sample_values: list[float]
) -> None:
    """create_performance_chart() falls back to line for candlestick."""
    # Candlestick requires OHLC data, so should fall back to line
    fig = create_performance_chart(
        sample_dates, sample_values, "EWLD.PA", chart_type="candlestick"
    )

    # Should still create a chart (line chart as fallback)
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1


def test_create_performance_chart_with_invalid_type(
    sample_dates: list[date], sample_values: list[float]
) -> None:
    """create_performance_chart() raises ValueError for invalid chart_type."""
    with pytest.raises(ValueError, match="Invalid chart_type"):
        create_performance_chart(
            sample_dates, sample_values, "EWLD.PA", chart_type="bar"
        )


def test_create_performance_chart_with_empty_data() -> None:
    """create_performance_chart() raises ValueError for empty data."""
    with pytest.raises(ValueError, match="cannot be empty"):
        create_performance_chart([], [], "EWLD.PA")


def test_create_performance_chart_with_mismatched_lengths(
    sample_dates: list[date],
) -> None:
    """create_performance_chart() raises ValueError for mismatched lengths."""
    with pytest.raises(ValueError, match="must have same length"):
        create_performance_chart(sample_dates, [100.0], "EWLD.PA")


# Chart theme tests
def test_apply_chart_theme_returns_figure(chart_preferences: ChartPreferences) -> None:
    """apply_chart_theme() returns modified Figure."""
    fig = go.Figure()
    result = apply_chart_theme(fig, chart_preferences)

    assert isinstance(result, go.Figure)


def test_apply_chart_theme_applies_grid_settings(
    chart_preferences: ChartPreferences,
) -> None:
    """apply_chart_theme() applies grid settings."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1, 2], y=[1, 2]))

    chart_preferences.show_grid = True
    result = apply_chart_theme(fig, chart_preferences)

    assert result.layout.xaxis.showgrid is True
    assert result.layout.yaxis.showgrid is True


def test_apply_chart_theme_applies_legend_settings(
    chart_preferences: ChartPreferences,
) -> None:
    """apply_chart_theme() applies legend settings."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1, 2], y=[1, 2], name="Test"))

    chart_preferences.show_legend = False
    result = apply_chart_theme(fig, chart_preferences)

    assert result.layout.showlegend is False


# Export tests
def test_export_chart_to_html_creates_file(tmp_path: Path) -> None:
    """export_chart_to_html() creates HTML file."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1, 2], y=[1, 2]))

    output_path = tmp_path / "chart.html"
    export_chart_to_html(fig, output_path)

    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_export_chart_to_html_creates_parent_directory(tmp_path: Path) -> None:
    """export_chart_to_html() creates parent directory if needed."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1, 2], y=[1, 2]))

    output_path = tmp_path / "subdir" / "chart.html"
    export_chart_to_html(fig, output_path)

    assert output_path.exists()
    assert output_path.parent.exists()


def test_export_chart_to_html_contains_valid_html(tmp_path: Path) -> None:
    """export_chart_to_html() creates valid HTML content."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1, 2], y=[1, 2]))

    output_path = tmp_path / "chart.html"
    export_chart_to_html(fig, output_path)

    content = output_path.read_text(encoding="utf-8")
    assert "<html>" in content
    assert "plotly" in content.lower()


def test_export_chart_to_png_raises_without_kaleido(tmp_path: Path) -> None:
    """export_chart_to_png() raises OSError if kaleido not installed."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1, 2], y=[1, 2]))

    output_path = tmp_path / "chart.png"

    # PNG export requires kaleido package which may not be installed
    # Should raise OSError if not available
    try:
        export_chart_to_png(fig, output_path)
        # If it succeeds, verify file was created
        assert output_path.exists()
    except OSError:
        # Expected if kaleido not installed
        pass


# Edge cases
def test_create_portfolio_value_chart_with_single_data_point() -> None:
    """create_portfolio_value_chart() handles single data point."""
    dates = [date(2024, 1, 1)]
    values = [10000.0]

    fig = create_portfolio_value_chart(dates, values)

    assert isinstance(fig, go.Figure)
    assert len(fig.data[0].x) == 1


def test_create_allocation_pie_chart_with_zero_values() -> None:
    """create_allocation_pie_chart() handles zero values."""
    tickers = ["EWLD.PA", "PE500.PA"]
    percentages = [0.0, 0.0]

    fig = create_allocation_pie_chart(tickers, percentages)

    assert isinstance(fig, go.Figure)


def test_create_risk_return_scatter_with_negative_returns() -> None:
    """create_risk_return_scatter() handles negative returns."""
    tickers = ["EWLD.PA", "PE500.PA"]
    returns = [-0.05, 0.10]
    volatilities = [0.15, 0.20]

    fig = create_risk_return_scatter(tickers, returns, volatilities)

    assert isinstance(fig, go.Figure)
    assert fig.data[0].y[0] == -5.0  # -0.05 * 100
