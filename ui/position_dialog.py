"""
Position dialog for adding or editing ETF positions.

Provides a modal dialog for creating new positions or editing existing ones.
"""

import logging
from datetime import date
from typing import Optional

from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import (
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from data.portfolio import ETFPosition

logger = logging.getLogger(__name__)


class PositionDialog(QDialog):
    """Dialog for adding or editing an ETF position."""

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        position: Optional[ETFPosition] = None,
        mode: str = "add",
    ) -> None:
        """
        Initialize position dialog.

        Args:
            parent: Parent widget.
            position: ETFPosition to edit (None for add mode).
            mode: "add" or "edit" mode.

        Example:
            >>> dialog = PositionDialog(None, mode="add")
            >>> if dialog.exec():
            ...     position = dialog.get_position()
        """
        super().__init__(parent)
        self.position = position
        self.mode = mode
        self._setup_ui()
        if position:
            self._populate_fields()
        logger.debug(f"Position dialog initialized in {mode} mode")

    def _setup_ui(self) -> None:
        """Create dialog UI elements."""
        # Set dialog title
        title = "Add Position" if self.mode == "add" else "Edit Position"
        self.setWindowTitle(title)
        self.setModal(True)

        # Create layout
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Ticker input
        self.ticker_input = QLineEdit()
        self.ticker_input.setPlaceholderText("e.g., EWLD.PA")
        if self.mode == "edit":
            self.ticker_input.setEnabled(False)  # Can't change ticker
        form_layout.addRow("Ticker:", self.ticker_input)

        # Name input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., Amundi MSCI World UCITS ETF")
        form_layout.addRow("Name:", self.name_input)

        # Quantity input
        self.quantity_input = QDoubleSpinBox()
        self.quantity_input.setRange(0.01, 999999.99)
        self.quantity_input.setDecimals(2)
        self.quantity_input.setValue(1.0)
        self.quantity_input.setSuffix(" shares")
        form_layout.addRow("Quantity:", self.quantity_input)

        # Buy price input
        self.buy_price_input = QDoubleSpinBox()
        self.buy_price_input.setRange(0.01, 999999.99)
        self.buy_price_input.setDecimals(2)
        self.buy_price_input.setValue(1.0)
        self.buy_price_input.setPrefix("€")
        form_layout.addRow("Buy Price:", self.buy_price_input)

        # Buy date input
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        form_layout.addRow("Buy Date:", self.date_input)

        layout.addLayout(form_layout)

        # Buttons
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)
        self.setMinimumWidth(400)

    def _populate_fields(self) -> None:
        """Populate dialog fields from existing position."""
        if not self.position:
            return

        self.ticker_input.setText(self.position.ticker)
        self.name_input.setText(self.position.name)
        self.quantity_input.setValue(self.position.quantity)
        self.buy_price_input.setValue(self.position.buy_price)

        # Convert date to QDate
        qdate = QDate(
            self.position.buy_date.year,
            self.position.buy_date.month,
            self.position.buy_date.day,
        )
        self.date_input.setDate(qdate)

        logger.debug(f"Fields populated from position: {self.position.ticker}")

    def _validate_input(self) -> bool:
        """
        Validate all input fields.

        Returns:
            True if all inputs are valid, False otherwise.
        """
        # Check ticker not empty
        if not self.ticker_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Ticker cannot be empty")
            return False

        # Check name not empty
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Name cannot be empty")
            return False

        # Check quantity > 0
        if self.quantity_input.value() <= 0:
            QMessageBox.warning(self, "Validation Error", "Quantity must be positive")
            return False

        # Check buy price > 0
        if self.buy_price_input.value() <= 0:
            QMessageBox.warning(self, "Validation Error", "Buy price must be positive")
            return False

        return True

    def accept(self) -> None:
        """Handle OK button click with validation."""
        if self._validate_input():
            logger.info(
                f"Position dialog accepted: {self.ticker_input.text()} "
                f"({self.mode} mode)"
            )
            super().accept()

    def get_position(self) -> ETFPosition:
        """
        Get ETFPosition from dialog fields.

        Returns:
            ETFPosition object with user input.

        Example:
            >>> dialog = PositionDialog(None, mode="add")
            >>> position = dialog.get_position()
            >>> print(position.ticker)
        """
        # Convert QDate to Python date
        qdate = self.date_input.date()
        buy_date = date(qdate.year(), qdate.month(), qdate.day())

        return ETFPosition(
            ticker=self.ticker_input.text().strip(),
            name=self.name_input.text().strip(),
            quantity=self.quantity_input.value(),
            buy_price=self.buy_price_input.value(),
            buy_date=buy_date,
        )
