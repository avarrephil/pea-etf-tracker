"""
Main application window for PEA ETF Tracker.

Provides menu bar, toolbar, tabbed interface for portfolio and charts.
"""

# mypy: disable-error-code="union-attr"

import logging
from pathlib import Path
from typing import Dict

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QStatusBar,
    QTabWidget,
)

from analytics.performance import (
    calculate_allocation,
    calculate_pnl,
    calculate_portfolio_value,
)
from config.settings import Settings, save_settings
from data.market_data import fetch_price
from data.portfolio import Portfolio
from ui.chart_widget import ChartWidget
from ui.dashboard import DashboardWidget
from ui.portfolio_table import PortfolioTableWidget
from visuals.charts import create_allocation_pie_chart

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window with menu, toolbar, tabs, and status bar."""

    def __init__(self, settings: Settings, portfolio: Portfolio) -> None:
        """
        Initialize main window.

        Args:
            settings: Application settings.
            portfolio: Portfolio to display.
        """
        super().__init__()
        self.settings = settings
        self.portfolio = portfolio
        self.prices: Dict[str, float] = {}

        self._setup_ui()
        self._load_geometry()

        # Auto-refresh timer
        if settings.auto_refresh_enabled:
            self._start_auto_refresh()

        logger.info("Main window initialized")

    def _setup_ui(self) -> None:
        """Create UI elements (menu, toolbar, tabs, status bar)."""
        self.setWindowTitle("PEA ETF Tracker v1.0")
        self._create_menu_bar()
        self._create_toolbar()
        self._create_central_widget()
        self._create_status_bar()

    def _create_menu_bar(self) -> None:
        """Create menu bar with File, Edit, View, Help menus."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        new_action = QAction("&New Portfolio", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self._new_portfolio)
        file_menu.addAction(new_action)

        open_action = QAction("&Open Portfolio...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._open_portfolio)
        file_menu.addAction(open_action)

        save_action = QAction("&Save Portfolio", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self._save_portfolio)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save Portfolio &As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self._save_portfolio_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        import_action = QAction("&Import CSV...", self)
        import_action.triggered.connect(self._import_csv)
        file_menu.addAction(import_action)

        export_action = QAction("&Export CSV...", self)
        export_action.triggered.connect(self._export_csv)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu("&Edit")

        add_position_action = QAction("&Add Position", self)
        add_position_action.setShortcut("Ctrl+A")
        add_position_action.triggered.connect(self._add_position)
        edit_menu.addAction(add_position_action)

        edit_menu.addSeparator()

        refresh_action = QAction("&Refresh Prices", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self._refresh_prices)
        edit_menu.addAction(refresh_action)

        edit_menu.addSeparator()

        settings_action = QAction("&Settings...", self)
        settings_action.setShortcut("Ctrl+,")
        settings_action.triggered.connect(self._show_settings)
        edit_menu.addAction(settings_action)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _create_toolbar(self) -> None:
        """Create toolbar with common actions."""
        toolbar = self.addToolBar("Main Toolbar")

        open_action = QAction("Open", self)
        open_action.triggered.connect(self._open_portfolio)
        toolbar.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self._save_portfolio)
        toolbar.addAction(save_action)

        toolbar.addSeparator()

        refresh_action = QAction("Refresh", self)
        refresh_action.triggered.connect(self._refresh_prices)
        toolbar.addAction(refresh_action)

    def _create_central_widget(self) -> None:
        """Create tab widget with Portfolio, Dashboard, and Charts tabs."""
        self.tabs = QTabWidget()

        # Portfolio tab
        self.portfolio_table = PortfolioTableWidget(self.portfolio)
        self.portfolio_table.position_edit_requested.connect(self._edit_position)
        self.portfolio_table.position_delete_requested.connect(self._delete_position)
        self.tabs.addTab(self.portfolio_table, "Portfolio")

        # Dashboard tab
        self.dashboard = DashboardWidget(portfolio=self.portfolio)
        self.tabs.addTab(self.dashboard, "Dashboard")

        # Charts tab
        self.chart_widget = ChartWidget(preferences=self.settings.chart_preferences)
        self.tabs.addTab(self.chart_widget, "Charts")

        self.setCentralWidget(self.tabs)

    def _create_status_bar(self) -> None:
        """Create status bar with portfolio value and P&L."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self._update_status_bar()

    def _update_status_bar(self) -> None:
        """Update status bar with current portfolio value and P&L."""
        if self.prices:
            total_value = calculate_portfolio_value(self.portfolio, self.prices)
            pnl = calculate_pnl(self.portfolio, self.prices)
            pnl_sign = "+" if pnl >= 0 else ""
            self.status_bar.showMessage(
                f"Portfolio Value: €{total_value:.2f} | P&L: {pnl_sign}€{pnl:.2f}"
            )
        else:
            self.status_bar.showMessage("Ready")

    def _start_auto_refresh(self) -> None:
        """Start auto-refresh timer for price updates."""
        interval_ms = self.settings.auto_refresh_interval_minutes * 60 * 1000
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self._refresh_prices)
        self.refresh_timer.start(interval_ms)
        logger.info(
            f"Auto-refresh enabled: {self.settings.auto_refresh_interval_minutes} min"
        )

    def _refresh_prices(self) -> None:
        """Fetch latest prices and update UI."""
        logger.info("Refreshing prices...")
        self.prices = {}

        for position in self.portfolio.get_all_positions():
            price = fetch_price(position.ticker, use_cache=True)
            if price:
                self.prices[position.ticker] = price

        # Update all components
        self.portfolio_table.update_prices(self.prices)
        self.dashboard.update_metrics(self.prices)
        self._update_charts()
        self._update_status_bar()

        logger.info(f"Prices refreshed for {len(self.prices)} positions")

    def _new_portfolio(self) -> None:
        """Create a new empty portfolio."""
        reply = QMessageBox.question(
            self,
            "New Portfolio",
            "Create new portfolio? Unsaved changes will be lost.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.portfolio = Portfolio()
            self.portfolio_table.set_portfolio(self.portfolio)
            self.dashboard.set_portfolio(self.portfolio)
            self.settings.last_portfolio_path = ""
            self.prices = {}
            self._update_status_bar()
            logger.info("Created new portfolio")

    def _open_portfolio(self) -> None:
        """Open portfolio from JSON file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Portfolio", "", "JSON Files (*.json)"
        )

        if file_path:
            try:
                self.portfolio = Portfolio.load_from_json(Path(file_path))
                self.portfolio_table.set_portfolio(self.portfolio)
                self.dashboard.set_portfolio(self.portfolio)
                self.settings.last_portfolio_path = file_path
                save_settings(self.settings)
                self.prices = {}
                self._update_status_bar()
                logger.info(f"Opened portfolio: {file_path}")
            except Exception as e:
                logger.error(f"Error opening portfolio: {e}")
                QMessageBox.critical(self, "Error", f"Could not open portfolio:\n{e}")

    def _save_portfolio(self) -> None:
        """Save portfolio to JSON file."""
        if self.settings.last_portfolio_path:
            self._save_to_file(Path(self.settings.last_portfolio_path))
        else:
            self._save_portfolio_as()

    def _save_portfolio_as(self) -> None:
        """Save portfolio to a new JSON file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Portfolio As", "", "JSON Files (*.json)"
        )

        if file_path:
            self._save_to_file(Path(file_path))
            self.settings.last_portfolio_path = file_path
            save_settings(self.settings)

    def _save_to_file(self, path: Path) -> None:
        """
        Save portfolio to file.

        Args:
            path: Path to save portfolio.
        """
        try:
            self.portfolio.save_to_json(path)
            logger.info(f"Saved portfolio: {path}")
            QMessageBox.information(self, "Success", "Portfolio saved successfully")
        except Exception as e:
            logger.error(f"Error saving portfolio: {e}")
            QMessageBox.critical(self, "Error", f"Could not save portfolio:\n{e}")

    def _import_csv(self) -> None:
        """Import portfolio from CSV file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import CSV", "", "CSV Files (*.csv)"
        )

        if file_path:
            try:
                self.portfolio = Portfolio.import_from_csv(Path(file_path))
                self.portfolio_table.set_portfolio(self.portfolio)
                self.dashboard.set_portfolio(self.portfolio)
                self.prices = {}
                self._update_status_bar()
                logger.info(f"Imported portfolio from CSV: {file_path}")
                QMessageBox.information(
                    self, "Success", "Portfolio imported successfully"
                )
            except Exception as e:
                logger.error(f"Error importing CSV: {e}")
                QMessageBox.critical(self, "Error", f"Could not import CSV:\n{e}")

    def _export_csv(self) -> None:
        """Export portfolio to CSV file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export CSV", "", "CSV Files (*.csv)"
        )

        if file_path:
            try:
                self.portfolio.export_to_csv(Path(file_path))
                logger.info(f"Exported portfolio to CSV: {file_path}")
                QMessageBox.information(
                    self, "Success", "Portfolio exported successfully"
                )
            except Exception as e:
                logger.error(f"Error exporting CSV: {e}")
                QMessageBox.critical(self, "Error", f"Could not export CSV:\n{e}")

    def _show_about(self) -> None:
        """Show About dialog."""
        QMessageBox.about(
            self,
            "About PEA ETF Tracker",
            "PEA ETF Tracker v1.0.0\n\n"
            "Track and analyze your PEA-eligible ETF portfolio.\n\n"
            "© 2024 Philippe Avarre",
        )

    def _add_position(self) -> None:
        """Show dialog to add new position."""
        from ui.position_dialog import PositionDialog

        dialog = PositionDialog(self, mode="add")
        if dialog.exec():
            try:
                position = dialog.get_position()
                self.portfolio.add_position(position)
                self.portfolio_table.set_portfolio(self.portfolio)
                self.dashboard.set_portfolio(self.portfolio)
                self._auto_save_portfolio()
                logger.info(f"Added position: {position.ticker}")
                QMessageBox.information(
                    self, "Success", f"Added position {position.ticker}"
                )
            except ValueError as e:
                logger.warning(f"Could not add position: {e}")
                QMessageBox.warning(self, "Error", f"Could not add position:\n{e}")

    def _edit_position(self, ticker: str) -> None:
        """Show dialog to edit position."""
        from ui.position_dialog import PositionDialog

        position = self.portfolio.get_position(ticker)
        if not position:
            QMessageBox.warning(self, "Error", f"Position {ticker} not found")
            return

        dialog = PositionDialog(self, position=position, mode="edit")
        if dialog.exec():
            try:
                new_position = dialog.get_position()
                self.portfolio.update_position(ticker, new_position)
                self.portfolio_table.set_portfolio(self.portfolio)
                self.dashboard.set_portfolio(self.portfolio)
                self._auto_save_portfolio()
                logger.info(f"Updated position: {ticker}")
                QMessageBox.information(self, "Success", f"Updated position {ticker}")
            except ValueError as e:
                logger.warning(f"Could not update position: {e}")
                QMessageBox.warning(self, "Error", f"Could not update position:\n{e}")

    def _delete_position(self, ticker: str) -> None:
        """Delete position after confirmation."""
        reply = QMessageBox.question(
            self,
            "Delete Position",
            f"Delete {ticker} from portfolio?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.portfolio.remove_position(ticker)
                self.portfolio_table.set_portfolio(self.portfolio)
                self.dashboard.set_portfolio(self.portfolio)
                self._auto_save_portfolio()
                logger.info(f"Deleted position: {ticker}")
                QMessageBox.information(self, "Success", f"Deleted position {ticker}")
            except ValueError as e:
                logger.warning(f"Could not delete position: {e}")
                QMessageBox.warning(self, "Error", f"Could not delete position:\n{e}")

    def _show_settings(self) -> None:
        """Show settings dialog."""
        from ui.settings_dialog import SettingsDialog

        dialog = SettingsDialog(self, self.settings)
        if dialog.exec():
            # Settings already saved in dialog.accept()
            self._apply_settings()
            logger.info("Settings updated")

    def _apply_settings(self) -> None:
        """Apply settings changes to UI."""
        # Restart auto-refresh timer if interval changed
        if hasattr(self, "refresh_timer"):
            self.refresh_timer.stop()
        if self.settings.auto_refresh_enabled:
            self._start_auto_refresh()

        # Update chart preferences
        self.chart_widget.preferences = self.settings.chart_preferences

        logger.debug("Settings applied to UI")

    def _auto_save_portfolio(self) -> None:
        """Auto-save portfolio to last used path."""
        if self.settings.last_portfolio_path:
            try:
                self.portfolio.save_to_json(Path(self.settings.last_portfolio_path))
                logger.debug("Portfolio auto-saved")
            except Exception as e:
                logger.warning(f"Auto-save failed: {e}")

    def _update_charts(self) -> None:
        """Update charts with latest data."""
        if not self.prices:
            return

        try:
            # Create allocation pie chart
            allocation = calculate_allocation(self.portfolio, self.prices)
            if allocation:
                tickers = list(allocation.keys())
                percentages = [allocation[t] * 100 for t in tickers]
                fig = create_allocation_pie_chart(tickers, percentages)
                self.chart_widget.display_chart(fig)
                logger.debug("Charts updated")
        except Exception as e:
            logger.warning(f"Could not update charts: {e}")

    def _load_geometry(self) -> None:
        """Load window geometry from settings."""
        geom = self.settings.window_geometry
        self.setGeometry(geom.x, geom.y, geom.width, geom.height)
        logger.debug("Window geometry loaded")

    def _save_geometry(self) -> None:
        """Save current window geometry to settings."""
        rect = self.geometry()
        self.settings.window_geometry.x = rect.x()
        self.settings.window_geometry.y = rect.y()
        self.settings.window_geometry.width = rect.width()
        self.settings.window_geometry.height = rect.height()
        logger.debug("Window geometry saved")

    def closeEvent(self, event) -> None:  # type: ignore
        """
        Handle window close event.

        Args:
            event: Close event.
        """
        self._save_geometry()
        save_settings(self.settings)
        logger.info("Application closed")
        event.accept()
