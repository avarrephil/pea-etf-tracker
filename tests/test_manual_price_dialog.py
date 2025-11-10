"""
Tests for ui.manual_price_dialog module.

Tests manual price dialog UI and validation.
"""

from datetime import date

import pytest
from pytestqt.qtbot import QtBot  # type: ignore

from ui.manual_price_dialog import ManualPriceDialog


def test_dialog_initialization_with_fetched_price(qtbot: QtBot) -> None:
    """Dialog initializes correctly with fetched price."""
    dialog = ManualPriceDialog(
        None,
        ticker="EWLD.PA",
        etf_name="Amundi World",
        current_price=29.35,
        is_manual=False,
        current_date=date(2024, 11, 9),
    )
    qtbot.addWidget(dialog)

    assert dialog.windowTitle() == "Set Manual Price"
    assert dialog.ticker == "EWLD.PA"
    assert dialog.current_price == 29.35
    assert not dialog.is_manual
    assert dialog.price_input.value() == 29.35


def test_dialog_initialization_with_manual_price(qtbot: QtBot) -> None:
    """Dialog initializes correctly with manual price."""
    dialog = ManualPriceDialog(
        None,
        ticker="PE500.PA",
        etf_name="Lyxor S&P 500",
        current_price=45.00,
        is_manual=True,
        current_date=date(2024, 11, 9),
    )
    qtbot.addWidget(dialog)

    assert dialog.current_price == 45.00
    assert dialog.is_manual
    assert dialog.clear_button.isEnabled()  # Clear button enabled for manual price


def test_dialog_validates_positive_price(qtbot: QtBot) -> None:
    """Dialog validates that QDoubleSpinBox enforces positive prices."""
    dialog = ManualPriceDialog(
        None,
        ticker="EWLD.PA",
        etf_name="Amundi World",
        current_price=29.35,
        is_manual=False,
        current_date=date(2024, 11, 9),
    )
    qtbot.addWidget(dialog)

    # QDoubleSpinBox has minimum of 0.01, so setting 0.0 clamps to 0.01
    dialog.price_input.setValue(0.0)

    # Value should be clamped to minimum (0.01)
    assert dialog.price_input.value() == 0.01
    # Validation should pass since it's > 0
    assert dialog._validate_input()


def test_dialog_accepts_positive_price(qtbot: QtBot) -> None:
    """Dialog accepts positive prices."""
    dialog = ManualPriceDialog(
        None,
        ticker="EWLD.PA",
        etf_name="Amundi World",
        current_price=29.35,
        is_manual=False,
        current_date=date(2024, 11, 9),
    )
    qtbot.addWidget(dialog)

    # Set valid price
    dialog.price_input.setValue(30.00)

    # Validation should pass
    assert dialog._validate_input()


def test_dialog_get_manual_price(qtbot: QtBot) -> None:
    """Dialog returns correct manual price after accept."""
    dialog = ManualPriceDialog(
        None,
        ticker="EWLD.PA",
        etf_name="Amundi World",
        current_price=29.35,
        is_manual=False,
        current_date=date(2024, 11, 9),
    )
    qtbot.addWidget(dialog)

    # Set new price
    dialog.price_input.setValue(32.50)
    dialog.accept()

    # Get manual price
    assert dialog.get_manual_price() == 32.50
    assert not dialog.is_cleared()


def test_dialog_clear_override_button(qtbot: QtBot) -> None:
    """Dialog clears manual price override when Clear Override clicked."""
    dialog = ManualPriceDialog(
        None,
        ticker="PE500.PA",
        etf_name="Lyxor S&P 500",
        current_price=45.00,
        is_manual=True,
        current_date=date(2024, 11, 9),
    )
    qtbot.addWidget(dialog)

    # Click Clear Override
    dialog._clear_override()

    # Check cleared state
    assert dialog.is_cleared()
    assert dialog.get_manual_price() is None


def test_dialog_clear_button_disabled_for_fetched_price(qtbot: QtBot) -> None:
    """Clear Override button is disabled when price is not manual."""
    dialog = ManualPriceDialog(
        None,
        ticker="EWLD.PA",
        etf_name="Amundi World",
        current_price=29.35,
        is_manual=False,
        current_date=date(2024, 11, 9),
    )
    qtbot.addWidget(dialog)

    # Clear button should be disabled for non-manual prices
    assert not dialog.clear_button.isEnabled()


def test_dialog_handles_none_current_price(qtbot: QtBot) -> None:
    """Dialog handles None current price gracefully."""
    dialog = ManualPriceDialog(
        None,
        ticker="EWLD.PA",
        etf_name="Amundi World",
        current_price=None,
        is_manual=False,
        current_date=date(2024, 11, 9),
    )
    qtbot.addWidget(dialog)

    # Should default to 1.0 if no current price
    assert dialog.price_input.value() == 1.0
