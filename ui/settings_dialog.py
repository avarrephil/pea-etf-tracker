"""
Settings dialog for configuring application preferences.

Provides a modal dialog for editing user settings including currency,
data source, auto-refresh, and chart preferences.
"""

import logging
from typing import Optional

from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from config.settings import Settings, get_default_settings, save_settings

logger = logging.getLogger(__name__)


class SettingsDialog(QDialog):
    """Dialog for editing application settings."""

    def __init__(
        self, parent: Optional[QWidget] = None, settings: Optional[Settings] = None
    ) -> None:
        """
        Initialize settings dialog.

        Args:
            parent: Parent widget.
            settings: Current application settings.

        Example:
            >>> dialog = SettingsDialog(None, settings)
            >>> if dialog.exec():
            ...     print("Settings saved")
        """
        super().__init__(parent)
        self.settings = settings or get_default_settings()
        self._setup_ui()
        self._populate_fields()
        logger.debug("Settings dialog initialized")

    def _setup_ui(self) -> None:
        """Create dialog UI elements."""
        self.setWindowTitle("Settings")
        self.setModal(True)

        layout = QVBoxLayout()

        # Create tab widget
        self.tabs = QTabWidget()

        # General tab
        general_tab = self._create_general_tab()
        self.tabs.addTab(general_tab, "General")

        # Charts tab
        charts_tab = self._create_charts_tab()
        self.tabs.addTab(charts_tab, "Charts")

        layout.addWidget(self.tabs)

        # Buttons
        button_layout = QVBoxLayout()

        # Restore defaults button
        self.restore_button = QPushButton("Restore Defaults")
        self.restore_button.clicked.connect(self._restore_defaults)
        button_layout.addWidget(self.restore_button)

        # Standard buttons
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Apply
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        apply_button = self.button_box.button(QDialogButtonBox.StandardButton.Apply)
        if apply_button:
            apply_button.clicked.connect(self._apply_settings)
        button_layout.addWidget(self.button_box)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

    def _create_general_tab(self) -> QWidget:
        """
        Create General settings tab.

        Returns:
            Widget with general settings controls.
        """
        tab = QWidget()
        layout = QVBoxLayout()

        # Currency settings
        currency_group = QGroupBox("Currency")
        currency_layout = QFormLayout()

        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["EUR", "USD", "GBP", "CHF"])
        currency_layout.addRow("Default Currency:", self.currency_combo)

        currency_group.setLayout(currency_layout)
        layout.addWidget(currency_group)

        # Data source settings
        data_group = QGroupBox("Data Source")
        data_layout = QFormLayout()

        self.data_source_combo = QComboBox()
        self.data_source_combo.addItems(["yfinance"])
        data_layout.addRow("Market Data Provider:", self.data_source_combo)

        data_group.setLayout(data_layout)
        layout.addWidget(data_group)

        # Auto-refresh settings
        refresh_group = QGroupBox("Auto-Refresh")
        refresh_layout = QFormLayout()

        self.auto_refresh_check = QCheckBox("Enable auto-refresh")
        refresh_layout.addRow(self.auto_refresh_check)

        self.refresh_interval_spin = QSpinBox()
        self.refresh_interval_spin.setRange(1, 60)
        self.refresh_interval_spin.setSuffix(" minutes")
        refresh_layout.addRow("Refresh Interval:", self.refresh_interval_spin)

        refresh_group.setLayout(refresh_layout)
        layout.addWidget(refresh_group)

        layout.addStretch()
        tab.setLayout(layout)
        return tab

    def _create_charts_tab(self) -> QWidget:
        """
        Create Charts settings tab.

        Returns:
            Widget with chart preference controls.
        """
        tab = QWidget()
        layout = QVBoxLayout()

        # Chart preferences
        chart_group = QGroupBox("Chart Preferences")
        chart_layout = QFormLayout()

        self.default_chart_combo = QComboBox()
        self.default_chart_combo.addItems(
            [
                "portfolio_value",
                "allocation_pie",
                "allocation_bar",
                "risk_return",
                "performance",
            ]
        )
        chart_layout.addRow("Default Chart:", self.default_chart_combo)

        self.color_scheme_combo = QComboBox()
        self.color_scheme_combo.addItems(["plotly", "pastel", "bold"])
        chart_layout.addRow("Color Scheme:", self.color_scheme_combo)

        self.show_grid_check = QCheckBox("Show grid")
        chart_layout.addRow(self.show_grid_check)

        self.show_legend_check = QCheckBox("Show legend")
        chart_layout.addRow(self.show_legend_check)

        chart_group.setLayout(chart_layout)
        layout.addWidget(chart_group)

        layout.addStretch()
        tab.setLayout(layout)
        return tab

    def _populate_fields(self) -> None:
        """Populate dialog fields from settings."""
        # General settings
        self.currency_combo.setCurrentText(self.settings.default_currency)
        self.data_source_combo.setCurrentText(self.settings.data_source)
        self.auto_refresh_check.setChecked(self.settings.auto_refresh_enabled)
        self.refresh_interval_spin.setValue(self.settings.auto_refresh_interval_minutes)

        # Chart preferences
        self.default_chart_combo.setCurrentText(
            self.settings.chart_preferences.default_chart
        )
        self.color_scheme_combo.setCurrentText(
            self.settings.chart_preferences.color_scheme
        )
        self.show_grid_check.setChecked(self.settings.chart_preferences.show_grid)
        self.show_legend_check.setChecked(self.settings.chart_preferences.show_legend)

        logger.debug("Settings dialog fields populated")

    def _update_settings_from_fields(self) -> None:
        """Update settings object from dialog fields."""
        # General settings
        self.settings.default_currency = self.currency_combo.currentText()
        self.settings.data_source = self.data_source_combo.currentText()
        self.settings.auto_refresh_enabled = self.auto_refresh_check.isChecked()
        self.settings.auto_refresh_interval_minutes = self.refresh_interval_spin.value()

        # Chart preferences
        self.settings.chart_preferences.default_chart = (
            self.default_chart_combo.currentText()
        )
        self.settings.chart_preferences.color_scheme = (
            self.color_scheme_combo.currentText()
        )
        self.settings.chart_preferences.show_grid = self.show_grid_check.isChecked()
        self.settings.chart_preferences.show_legend = self.show_legend_check.isChecked()

        logger.debug("Settings updated from dialog fields")

    def _apply_settings(self) -> None:
        """Apply settings without closing dialog."""
        self._update_settings_from_fields()
        try:
            save_settings(self.settings)
            logger.info("Settings applied")
            QMessageBox.information(self, "Settings", "Settings applied successfully")
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            QMessageBox.critical(self, "Error", f"Could not save settings:\n{e}")

    def _restore_defaults(self) -> None:
        """Restore default settings after confirmation."""
        reply = QMessageBox.question(
            self,
            "Restore Defaults",
            "Reset all settings to defaults?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.settings = get_default_settings()
            self._populate_fields()
            logger.info("Settings restored to defaults")

    def accept(self) -> None:
        """Save settings and close dialog."""
        self._update_settings_from_fields()
        try:
            save_settings(self.settings)
            logger.info("Settings saved")
            super().accept()
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            QMessageBox.critical(self, "Error", f"Could not save settings:\n{e}")
