"""
Dashboard widget with portfolio KPIs and metrics.

Displays key performance indicators, risk metrics, and summary statistics.
"""

import logging
from typing import Dict, Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from analytics.performance import calculate_pnl, calculate_portfolio_value
from data.portfolio import Portfolio

logger = logging.getLogger(__name__)


class DashboardWidget(QWidget):
    """Dashboard widget with portfolio KPIs and metrics."""

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        portfolio: Optional[Portfolio] = None,
    ) -> None:
        """
        Initialize dashboard widget.

        Args:
            parent: Parent widget.
            portfolio: Portfolio to display metrics for.

        Example:
            >>> dashboard = DashboardWidget(portfolio=portfolio)
            >>> dashboard.update_metrics(prices)
        """
        super().__init__(parent)
        self.portfolio = portfolio or Portfolio()
        self.prices: Dict[str, float] = {}
        self._setup_ui()
        logger.debug("Dashboard widget initialized")

    def _setup_ui(self) -> None:
        """Create dashboard UI elements."""
        layout = QVBoxLayout()

        # KPI Cards
        kpi_group = QGroupBox("Portfolio Overview")
        kpi_layout = QGridLayout()

        # Total Value
        total_value_label = QLabel("Total Value:")
        total_value_label.setStyleSheet("font-weight: bold;")
        self.total_value_display = QLabel("—")
        self.total_value_display.setStyleSheet("font-size: 18px; color: #1f77b4;")
        kpi_layout.addWidget(total_value_label, 0, 0)
        kpi_layout.addWidget(self.total_value_display, 0, 1)

        # Total Invested
        total_invested_label = QLabel("Total Invested:")
        total_invested_label.setStyleSheet("font-weight: bold;")
        self.total_invested_display = QLabel("—")
        self.total_invested_display.setStyleSheet("font-size: 18px;")
        kpi_layout.addWidget(total_invested_label, 1, 0)
        kpi_layout.addWidget(self.total_invested_display, 1, 1)

        # Total P&L
        pnl_label = QLabel("Total P&L:")
        pnl_label.setStyleSheet("font-weight: bold;")
        self.pnl_display = QLabel("—")
        self.pnl_display.setStyleSheet("font-size: 18px;")
        kpi_layout.addWidget(pnl_label, 2, 0)
        kpi_layout.addWidget(self.pnl_display, 2, 1)

        # P&L Percentage
        pnl_pct_label = QLabel("P&L %:")
        pnl_pct_label.setStyleSheet("font-weight: bold;")
        self.pnl_pct_display = QLabel("—")
        self.pnl_pct_display.setStyleSheet("font-size: 18px;")
        kpi_layout.addWidget(pnl_pct_label, 3, 0)
        kpi_layout.addWidget(self.pnl_pct_display, 3, 1)

        # Number of Positions
        positions_label = QLabel("Positions:")
        positions_label.setStyleSheet("font-weight: bold;")
        self.positions_display = QLabel("—")
        self.positions_display.setStyleSheet("font-size: 18px;")
        kpi_layout.addWidget(positions_label, 4, 0)
        kpi_layout.addWidget(self.positions_display, 4, 1)

        kpi_group.setLayout(kpi_layout)
        layout.addWidget(kpi_group)

        # Status message
        self.status_label = QLabel("Refresh prices to see metrics")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(self.status_label)

        layout.addStretch()
        self.setLayout(layout)

        # Initial update
        self._update_display()

    def _update_display(self) -> None:
        """Update dashboard display with current data."""
        # Number of positions (always available)
        num_positions = len(self.portfolio.get_all_positions())
        self.positions_display.setText(str(num_positions))

        if not self.prices:
            # No prices available
            self.total_value_display.setText("—")
            self.total_invested_display.setText("—")
            self.pnl_display.setText("—")
            self.pnl_pct_display.setText("—")
            self.status_label.setText("Refresh prices to see metrics")
            return

        # Calculate total invested
        total_invested = sum(
            pos.quantity * pos.buy_price for pos in self.portfolio.get_all_positions()
        )
        self.total_invested_display.setText(f"€{total_invested:,.2f}")

        # Calculate current value
        total_value = calculate_portfolio_value(self.portfolio, self.prices)
        self.total_value_display.setText(f"€{total_value:,.2f}")

        # Calculate P&L
        pnl = calculate_pnl(self.portfolio, self.prices)
        pnl_color = "#2ca02c" if pnl >= 0 else "#d62728"  # green or red
        self.pnl_display.setText(f"€{pnl:+,.2f}")
        self.pnl_display.setStyleSheet(f"font-size: 18px; color: {pnl_color};")

        # Calculate P&L percentage
        pnl_pct = (pnl / total_invested * 100) if total_invested > 0 else 0.0
        self.pnl_pct_display.setText(f"{pnl_pct:+.2f}%")
        self.pnl_pct_display.setStyleSheet(f"font-size: 18px; color: {pnl_color};")

        # Update status
        self.status_label.setText(f"Last updated with {len(self.prices)} price(s)")

        logger.debug("Dashboard display updated")

    def update_metrics(self, prices: Dict[str, float]) -> None:
        """
        Update dashboard with latest prices.

        Args:
            prices: Dictionary mapping ticker to current price.

        Example:
            >>> dashboard.update_metrics({"EWLD.PA": 29.35, "PE500.PA": 43.12})
        """
        self.prices = prices
        self._update_display()
        logger.info(f"Dashboard metrics updated with {len(prices)} prices")

    def set_portfolio(self, portfolio: Portfolio) -> None:
        """
        Set a new portfolio and refresh the dashboard.

        Args:
            portfolio: New portfolio to display.

        Example:
            >>> dashboard.set_portfolio(new_portfolio)
        """
        self.portfolio = portfolio
        self.prices = {}  # Clear prices when portfolio changes
        self._update_display()
        logger.info("Dashboard portfolio updated")
