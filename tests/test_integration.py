"""
Integration tests for PyQt6 GUI.

Tests main window, portfolio table, and UI interactions.
"""

from datetime import date
from pathlib import Path

import pytest
from pytestqt.qtbot import QtBot

from config.settings import get_default_settings
from data.portfolio import ETFPosition, Portfolio
from ui.main_window import MainWindow
from ui.portfolio_table import PortfolioTableWidget


# Fixtures
@pytest.fixture
def sample_portfolio() -> Portfolio:
    """Create sample portfolio for testing."""
    positions = [
        ETFPosition("EWLD.PA", "Amundi World", 100.0, 28.50, date(2024, 1, 15)),
        ETFPosition("PE500.PA", "Lyxor S&P 500", 50.0, 42.30, date(2024, 2, 10)),
    ]
    return Portfolio(positions)


# MainWindow tests
def test_main_window_opens(qtbot: QtBot, sample_portfolio: Portfolio) -> None:
    """MainWindow opens and displays without errors."""
    settings = get_default_settings()
    window = MainWindow(settings, sample_portfolio)
    qtbot.addWidget(window)
    window.show()

    assert window.isVisible()
    assert window.windowTitle() == "PEA ETF Tracker v1.0"


def test_main_window_has_menu_bar(qtbot: QtBot, sample_portfolio: Portfolio) -> None:
    """MainWindow has menu bar with File, Edit, Help menus."""
    settings = get_default_settings()
    window = MainWindow(settings, sample_portfolio)
    qtbot.addWidget(window)

    menubar = window.menuBar()
    assert menubar is not None

    # Check menu titles
    menus = [action.text() for action in menubar.actions()]
    assert "&File" in menus
    assert "&Edit" in menus
    assert "&Help" in menus


def test_main_window_has_toolbar(qtbot: QtBot, sample_portfolio: Portfolio) -> None:
    """MainWindow has toolbar with common actions."""
    settings = get_default_settings()
    window = MainWindow(settings, sample_portfolio)
    qtbot.addWidget(window)

    # Check toolbar exists
    toolbars = window.findChildren(type(window.addToolBar("test")))
    assert len(toolbars) > 0


def test_main_window_has_status_bar(qtbot: QtBot, sample_portfolio: Portfolio) -> None:
    """MainWindow has status bar."""
    settings = get_default_settings()
    window = MainWindow(settings, sample_portfolio)
    qtbot.addWidget(window)

    status_bar = window.statusBar()
    assert status_bar is not None
    assert status_bar.currentMessage() == "Ready"


def test_main_window_has_tabs(qtbot: QtBot, sample_portfolio: Portfolio) -> None:
    """MainWindow has tab widget with Portfolio tab."""
    settings = get_default_settings()
    window = MainWindow(settings, sample_portfolio)
    qtbot.addWidget(window)

    assert window.tabs is not None
    assert window.tabs.count() >= 1
    assert window.tabs.tabText(0) == "Portfolio"


def test_main_window_saves_geometry_on_close(
    qtbot: QtBot, sample_portfolio: Portfolio
) -> None:
    """MainWindow saves geometry when closed."""
    settings = get_default_settings()
    original_width = settings.window_geometry.width

    window = MainWindow(settings, sample_portfolio)
    qtbot.addWidget(window)
    window.show()

    # Resize window
    window.resize(1400, 900)

    # Close window
    window.close()

    # Check geometry was saved
    assert window.settings.window_geometry.width == 1400
    assert window.settings.window_geometry.height == 900


# PortfolioTableWidget tests
def test_portfolio_table_displays_positions(
    qtbot: QtBot, sample_portfolio: Portfolio
) -> None:
    """Portfolio table displays all positions correctly."""
    table = PortfolioTableWidget(sample_portfolio)
    qtbot.addWidget(table)

    assert table.rowCount() == 2
    assert table.columnCount() == 7

    # Check first row
    assert table.item(0, 0).text() == "EWLD.PA"
    assert table.item(0, 1).text() == "Amundi World"
    assert table.item(0, 2).text() == "100.0"
    assert table.item(0, 3).text() == "28.50"

    # Check second row
    assert table.item(1, 0).text() == "PE500.PA"
    assert table.item(1, 1).text() == "Lyxor S&P 500"


def test_portfolio_table_has_correct_headers(qtbot: QtBot) -> None:
    """Portfolio table has correct column headers."""
    portfolio = Portfolio()
    table = PortfolioTableWidget(portfolio)
    qtbot.addWidget(table)

    headers = [table.horizontalHeaderItem(i).text() for i in range(table.columnCount())]

    assert "Ticker" in headers
    assert "Name" in headers
    assert "Quantity" in headers
    assert "Buy Price (€)" in headers
    assert "Current Price (€)" in headers
    assert "P&L (€)" in headers
    assert "P&L %" in headers


def test_portfolio_table_updates_prices(
    qtbot: QtBot, sample_portfolio: Portfolio
) -> None:
    """Portfolio table updates when prices provided."""
    table = PortfolioTableWidget(sample_portfolio)
    qtbot.addWidget(table)

    # Initial state - no current prices
    assert table.item(0, 4).text() == "-"
    assert table.item(0, 5).text() == "-"
    assert table.item(0, 6).text() == "-"

    # Update prices
    prices = {"EWLD.PA": 29.35, "PE500.PA": 43.12}
    table.update_prices(prices)

    # Check current prices updated
    assert table.item(0, 4).text() == "29.35"
    assert table.item(1, 4).text() == "43.12"

    # Check P&L calculated
    # EWLD.PA: (100 * 29.35) - (100 * 28.50) = 2935 - 2850 = +85.00
    assert table.item(0, 5).text() == "+85.00"

    # Check P&L % calculated
    # EWLD.PA: (85 / 2850) * 100 = 2.98%
    pnl_pct = table.item(0, 6).text()
    assert pnl_pct.startswith("+")
    assert "%" in pnl_pct


def test_portfolio_table_with_empty_portfolio(qtbot: QtBot) -> None:
    """Portfolio table handles empty portfolio."""
    portfolio = Portfolio()
    table = PortfolioTableWidget(portfolio)
    qtbot.addWidget(table)

    assert table.rowCount() == 0


def test_portfolio_table_set_portfolio(
    qtbot: QtBot, sample_portfolio: Portfolio
) -> None:
    """Portfolio table can be updated with new portfolio."""
    # Start with empty portfolio
    table = PortfolioTableWidget(Portfolio())
    qtbot.addWidget(table)
    assert table.rowCount() == 0

    # Set new portfolio
    table.set_portfolio(sample_portfolio)

    # Check table updated
    assert table.rowCount() == 2
    assert table.item(0, 0).text() == "EWLD.PA"


def test_portfolio_table_is_read_only(
    qtbot: QtBot, sample_portfolio: Portfolio
) -> None:
    """Portfolio table is read-only (no edit triggers)."""
    table = PortfolioTableWidget(sample_portfolio)
    qtbot.addWidget(table)

    # Table should have no edit triggers
    from PyQt6.QtWidgets import QAbstractItemView

    assert table.editTriggers() == QAbstractItemView.EditTrigger.NoEditTriggers


def test_portfolio_table_sorting_enabled(
    qtbot: QtBot, sample_portfolio: Portfolio
) -> None:
    """Portfolio table has sorting enabled."""
    table = PortfolioTableWidget(sample_portfolio)
    qtbot.addWidget(table)

    assert table.isSortingEnabled()


# Integration tests - Main window with portfolio table
def test_main_window_updates_status_bar_with_prices(
    qtbot: QtBot, sample_portfolio: Portfolio
) -> None:
    """Main window updates status bar when prices refreshed."""
    settings = get_default_settings()
    window = MainWindow(settings, sample_portfolio)
    qtbot.addWidget(window)

    # Initial status
    assert window.statusBar().currentMessage() == "Ready"

    # Set prices manually
    window.prices = {"EWLD.PA": 29.35, "PE500.PA": 43.12}
    window._update_status_bar()

    # Check status bar updated
    status_text = window.statusBar().currentMessage()
    assert "Portfolio Value:" in status_text
    assert "P&L:" in status_text


def test_main_window_portfolio_table_integration(
    qtbot: QtBot, sample_portfolio: Portfolio
) -> None:
    """Main window contains portfolio table with correct data."""
    settings = get_default_settings()
    window = MainWindow(settings, sample_portfolio)
    qtbot.addWidget(window)

    # Access portfolio table from main window
    portfolio_table = window.portfolio_table

    assert portfolio_table is not None
    assert portfolio_table.rowCount() == 2
    assert portfolio_table.item(0, 0).text() == "EWLD.PA"


def test_main_window_loads_geometry_from_settings(qtbot: QtBot) -> None:
    """Main window loads geometry from settings."""
    settings = get_default_settings()
    settings.window_geometry.width = 1400
    settings.window_geometry.height = 900
    settings.window_geometry.x = 50
    settings.window_geometry.y = 50

    portfolio = Portfolio()
    window = MainWindow(settings, portfolio)
    qtbot.addWidget(window)

    # Check geometry loaded
    geom = window.geometry()
    assert geom.width() == 1400
    assert geom.height() == 900
