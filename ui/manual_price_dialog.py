"""
Manual price override dialog for ETF positions.

Provides a dialog for setting or clearing manual price overrides.
"""

import logging
from datetime import date
from typing import Optional

from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

logger = logging.getLogger(__name__)


class ManualPriceDialog(QDialog):
    """Dialog for setting or clearing manual price override."""

    def __init__(
        self,
        parent: Optional[QWidget],
        ticker: str,
        etf_name: str,
        current_price: Optional[float],
        is_manual: bool,
        current_date: date,
    ) -> None:
        """
        Initialize manual price dialog.

        Args:
            parent: Parent widget.
            ticker: ETF ticker symbol.
            etf_name: ETF name.
            current_price: Current price (manual or fetched).
            is_manual: Whether current price is manually overridden.
            current_date: Current date for display.

        Example:
            >>> dialog = ManualPriceDialog(
            ...     None, "EWLD.PA", "Amundi World", 29.35, False, date.today()
            ... )
            >>> if dialog.exec():
            ...     new_price = dialog.get_manual_price()
        """
        super().__init__(parent)
        self.ticker = ticker
        self.etf_name = etf_name
        self.current_price = current_price
        self.is_manual = is_manual
        self.current_date = current_date
        self._manual_price: Optional[float] = None
        self._cleared = False
        self._setup_ui()
        logger.debug("Manual price dialog initialized for %s", ticker)

    def _setup_ui(self) -> None:
        """Create dialog UI elements."""
        self.setWindowTitle("Set Manual Price")
        self.setModal(True)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Ticker (read-only)
        ticker_label = QLabel(self.ticker)
        ticker_label.setStyleSheet("font-weight: bold;")
        form_layout.addRow("Ticker:", ticker_label)

        # ETF Name (read-only)
        name_label = QLabel(self.etf_name)
        form_layout.addRow("Name:", name_label)

        # Current Price (read-only with source indicator)
        if self.current_price is not None:
            price_text = f"€{self.current_price:.2f}"
            if self.is_manual:
                price_text += " (Manual)"
                current_price_label = QLabel(price_text)
                current_price_label.setStyleSheet("color: #2ca02c; font-weight: bold;")
            else:
                price_text += " (Live/Cached)"
                current_price_label = QLabel(price_text)
        else:
            current_price_label = QLabel("—")
        form_layout.addRow("Current Price:", current_price_label)

        # Date (read-only)
        date_label = QLabel(self.current_date.strftime("%Y-%m-%d"))
        form_layout.addRow("Date:", date_label)

        layout.addLayout(form_layout)

        # New Manual Price input
        price_layout = QFormLayout()
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0.01, 999999.99)
        self.price_input.setDecimals(2)
        self.price_input.setPrefix("€")
        if self.current_price is not None:
            self.price_input.setValue(self.current_price)
        else:
            self.price_input.setValue(1.0)
        price_layout.addRow("New Manual Price:", self.price_input)

        layout.addLayout(price_layout)

        # Buttons
        button_layout = QVBoxLayout()

        # Standard OK/Cancel buttons
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Clear Override button (separate)
        self.clear_button = QPushButton("Clear Override")
        self.clear_button.clicked.connect(self._clear_override)
        self.clear_button.setEnabled(
            self.is_manual
        )  # Only enabled if manual price exists

        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.button_box)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.setMinimumWidth(400)

    def _validate_input(self) -> bool:
        """
        Validate manual price input.

        Returns:
            True if input is valid, False otherwise.
        """
        if self.price_input.value() <= 0:
            QMessageBox.warning(
                self, "Validation Error", "Price must be positive and greater than zero"
            )
            return False
        return True

    def _clear_override(self) -> None:
        """Handle Clear Override button click."""
        self._cleared = True
        self._manual_price = None
        logger.info("Manual price override cleared for %s", self.ticker)
        super().accept()

    def accept(self) -> None:
        """Handle OK button click with validation."""
        if self._validate_input():
            self._manual_price = self.price_input.value()
            logger.info(
                "Manual price set for %s: €%.2f", self.ticker, self._manual_price
            )
            super().accept()

    def get_manual_price(self) -> Optional[float]:
        """
        Get the manual price from dialog.

        Returns:
            Manual price if set, None if cleared.

        Example:
            >>> dialog = ManualPriceDialog(...)
            >>> if dialog.exec():
            ...     price = dialog.get_manual_price()
        """
        return self._manual_price

    def is_cleared(self) -> bool:
        """
        Check if manual price override was cleared.

        Returns:
            True if override was cleared, False otherwise.

        Example:
            >>> if dialog.is_cleared():
            ...     # Remove manual override
        """
        return self._cleared
