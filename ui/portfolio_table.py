"""
Portfolio table widget with CRUD operations.

Displays portfolio positions in a table with columns for ticker, name, quantity,
buy price, current price, P&L, and P&L percentage.
"""

import logging
from typing import Dict

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QBrush, QColor
from PyQt6.QtWidgets import QHeaderView, QMenu, QTableWidget, QTableWidgetItem

from data.portfolio import Portfolio

logger = logging.getLogger(__name__)


class PortfolioTableWidget(QTableWidget):
    """Table widget displaying portfolio positions."""

    # Signals
    position_edit_requested = pyqtSignal(str)  # ticker
    position_delete_requested = pyqtSignal(str)  # ticker
    manual_price_requested = pyqtSignal(str)  # ticker

    def __init__(self, portfolio: Portfolio) -> None:
        """
        Initialize portfolio table.

        Args:
            portfolio: Portfolio to display.
        """
        super().__init__()
        self.portfolio = portfolio
        self._setup_table()
        self._setup_context_menu()
        self._setup_double_click()
        self._populate_table()
        logger.debug("Portfolio table initialized")

    def _setup_double_click(self) -> None:
        """Set up double-click handler for Current Price column."""
        self.cellDoubleClicked.connect(self._on_cell_double_click)

    def _setup_table(self) -> None:
        """Configure table columns and headers."""
        self.setColumnCount(7)
        self.setHorizontalHeaderLabels(
            [
                "Ticker",
                "Name",
                "Quantity",
                "Buy Price (€)",
                "Current Price (€)",
                "P&L (€)",
                "P&L %",
            ]
        )

        # Configure column sizing
        header = self.horizontalHeader()
        if header:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Enable sorting
        self.setSortingEnabled(True)

        # Make table read-only
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    def _setup_context_menu(self) -> None:
        """Set up right-click context menu."""
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

    def _populate_table(self) -> None:
        """Populate table with portfolio positions."""
        positions = self.portfolio.get_all_positions()
        self.setRowCount(len(positions))

        for row, position in enumerate(positions):
            # Ticker
            self.setItem(row, 0, QTableWidgetItem(position.ticker))

            # Name
            self.setItem(row, 1, QTableWidgetItem(position.name))

            # Quantity
            quantity_item = QTableWidgetItem(str(position.quantity))
            quantity_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            self.setItem(row, 2, quantity_item)

            # Buy Price
            buy_price_item = QTableWidgetItem(f"{position.buy_price:.2f}")
            buy_price_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            self.setItem(row, 3, buy_price_item)

            # Current price, P&L, P&L% will be filled when prices are updated
            self.setItem(row, 4, QTableWidgetItem("-"))
            self.setItem(row, 5, QTableWidgetItem("-"))
            self.setItem(row, 6, QTableWidgetItem("-"))

    def _on_cell_double_click(self, row: int, column: int) -> None:
        """
        Handle double-click on table cell.

        Args:
            row: Row index.
            column: Column index.
        """
        # Only handle double-click on Current Price column (column 4)
        if column == 4:
            ticker_item = self.item(row, 0)
            if ticker_item:
                ticker = ticker_item.text()
                self.manual_price_requested.emit(ticker)
                logger.debug("Manual price requested for %s", ticker)

    def update_prices(self, prices: Dict[str, float]) -> None:
        """
        Update current prices and recalculate P&L for all positions.

        Uses manual price override if set, otherwise uses fetched price.

        Args:
            prices: Dictionary mapping ticker to fetched price.
        """
        for row in range(self.rowCount()):
            ticker_item = self.item(row, 0)
            if ticker_item:
                ticker = ticker_item.text()
                position = self.portfolio.get_position(ticker)

                if position:
                    # Determine effective price (manual override or fetched)
                    if position.manual_price is not None:
                        # Use manual price
                        current_price = position.manual_price
                        is_manual = True
                    elif ticker in prices:
                        # Use fetched price
                        current_price = prices[ticker]
                        is_manual = False
                    else:
                        # No price available
                        continue

                    # Current Price
                    current_price_item = QTableWidgetItem(f"{current_price:.2f}")
                    current_price_item.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                    )

                    # Visual indicator for manual prices
                    if is_manual:
                        current_price_item.setBackground(QBrush(QColor("#90EE90")))
                        current_price_item.setToolTip("Manual Price (overridden)")

                    self.setItem(row, 4, current_price_item)

                    # Calculate P&L using effective price
                    invested = position.quantity * position.buy_price
                    current_value = position.quantity * current_price
                    pnl = current_value - invested
                    pnl_pct = (pnl / invested * 100) if invested > 0 else 0.0

                    # P&L (€)
                    pnl_item = QTableWidgetItem(f"{pnl:+.2f}")
                    pnl_item.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                    )
                    self.setItem(row, 5, pnl_item)

                    # P&L %
                    pnl_pct_item = QTableWidgetItem(f"{pnl_pct:+.2f}%")
                    pnl_pct_item.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                    )
                    self.setItem(row, 6, pnl_pct_item)

                    price_source = "manual" if is_manual else "fetched"
                    logger.debug(
                        "Updated prices for %s: %.2f (%s)",
                        ticker,
                        current_price,
                        price_source,
                    )

    def _show_context_menu(self, position) -> None:  # type: ignore
        """
        Show context menu for selected row.

        Args:
            position: Click position.
        """
        row = self.rowAt(position.y())
        if row < 0:
            return

        ticker_item = self.item(row, 0)
        if not ticker_item:
            return

        ticker = ticker_item.text()

        menu = QMenu(self)

        edit_action = QAction("Edit Position", self)
        edit_action.triggered.connect(lambda: self.position_edit_requested.emit(ticker))
        menu.addAction(edit_action)

        delete_action = QAction("Delete Position", self)
        delete_action.triggered.connect(
            lambda: self.position_delete_requested.emit(ticker)
        )
        menu.addAction(delete_action)

        viewport = self.viewport()
        if viewport:
            menu.exec(viewport.mapToGlobal(position))
        logger.debug(f"Context menu shown for {ticker}")

    def set_portfolio(self, portfolio: Portfolio) -> None:
        """
        Set a new portfolio and refresh the table.

        Args:
            portfolio: New portfolio to display.
        """
        self.portfolio = portfolio
        self._populate_table()
        logger.info("Portfolio table updated with new portfolio")
