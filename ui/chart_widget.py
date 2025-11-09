"""
Chart widget for displaying Plotly charts.

Provides a widget for displaying interactive Plotly charts using QWebEngineView.
"""

import logging
from pathlib import Path
from typing import Optional

import plotly.graph_objects as go
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView

    HAS_WEBENGINE = True
except ImportError:
    HAS_WEBENGINE = False
    QWebEngineView = None  # type: ignore

from config.settings import ChartPreferences
from visuals.charts import apply_chart_theme, export_chart_to_html, export_chart_to_png

logger = logging.getLogger(__name__)


class ChartWidget(QWidget):
    """Widget for displaying Plotly charts."""

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        preferences: Optional[ChartPreferences] = None,
    ) -> None:
        """
        Initialize chart widget.

        Args:
            parent: Parent widget.
            preferences: Chart preferences for theming.

        Example:
            >>> widget = ChartWidget()
            >>> fig = go.Figure()
            >>> widget.display_chart(fig)
        """
        super().__init__(parent)
        self.preferences = preferences or ChartPreferences(
            default_chart="portfolio_value",
            color_scheme="plotly",
            show_grid=True,
            show_legend=True,
        )
        self.current_fig: Optional[go.Figure] = None
        self._setup_ui()
        logger.debug("Chart widget initialized")

    def _setup_ui(self) -> None:
        """Create UI elements."""
        layout = QVBoxLayout()

        # Top controls
        controls_layout = QHBoxLayout()

        # Chart type selector
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(
            [
                "Portfolio Value",
                "Allocation Pie",
                "Allocation Bar",
                "Risk vs Return",
                "Performance",
            ]
        )
        self.chart_type_combo.currentTextChanged.connect(self._on_chart_type_changed)
        controls_layout.addWidget(self.chart_type_combo)

        controls_layout.addStretch()

        # Export buttons
        self.export_png_button = QPushButton("Export PNG")
        self.export_png_button.clicked.connect(self._export_png)
        controls_layout.addWidget(self.export_png_button)

        self.export_html_button = QPushButton("Export HTML")
        self.export_html_button.clicked.connect(self._export_html)
        controls_layout.addWidget(self.export_html_button)

        layout.addLayout(controls_layout)

        # Web view for chart display (or placeholder if WebEngine not available)
        if HAS_WEBENGINE and QWebEngineView:
            self.web_view = QWebEngineView()
            self.web_view.setMinimumHeight(400)
            layout.addWidget(self.web_view)
        else:
            self.web_view = None  # type: ignore
            placeholder = QLabel(
                "Chart display requires PyQt6-WebEngine.\n"
                "Charts can still be exported to PNG/HTML."
            )
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            placeholder.setMinimumHeight(400)
            layout.addWidget(placeholder)

        self.setLayout(layout)

        # Initially disable export buttons
        self.export_png_button.setEnabled(False)
        self.export_html_button.setEnabled(False)

    def _on_chart_type_changed(self, chart_type: str) -> None:
        """
        Handle chart type selection change.

        Args:
            chart_type: Selected chart type name.
        """
        logger.debug(f"Chart type changed to: {chart_type}")
        # This would trigger chart update in main window
        # For now, just log the change

    def display_chart(self, fig: go.Figure) -> None:
        """
        Display Plotly figure in web view.

        Args:
            fig: Plotly Figure to display.

        Example:
            >>> import plotly.graph_objects as go
            >>> fig = go.Figure(data=[go.Bar(x=[1, 2, 3], y=[4, 5, 6])])
            >>> widget.display_chart(fig)
        """
        # Store current figure for export
        self.current_fig = fig

        # Apply theme
        fig = apply_chart_theme(fig, self.preferences)

        # Convert to HTML and display in web view (if available)
        if self.web_view:
            html = fig.to_html(include_plotlyjs="cdn")
            self.web_view.setHtml(html)

        # Enable export buttons
        self.export_png_button.setEnabled(True)
        self.export_html_button.setEnabled(True)

        logger.info("Chart displayed")

    def _export_png(self) -> None:
        """Export current chart to PNG file."""
        if not self.current_fig:
            QMessageBox.warning(self, "Export Error", "No chart to export")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Chart as PNG", "", "PNG Files (*.png)"
        )

        if file_path:
            try:
                export_chart_to_png(self.current_fig, Path(file_path))
                logger.info(f"Chart exported to PNG: {file_path}")
                QMessageBox.information(
                    self, "Export Successful", f"Chart saved to:\n{file_path}"
                )
            except Exception as e:
                logger.error(f"Error exporting PNG: {e}")
                QMessageBox.critical(
                    self, "Export Error", f"Could not export chart:\n{e}"
                )

    def _export_html(self) -> None:
        """Export current chart to HTML file."""
        if not self.current_fig:
            QMessageBox.warning(self, "Export Error", "No chart to export")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Chart as HTML", "", "HTML Files (*.html)"
        )

        if file_path:
            try:
                export_chart_to_html(self.current_fig, Path(file_path))
                logger.info(f"Chart exported to HTML: {file_path}")
                QMessageBox.information(
                    self, "Export Successful", f"Chart saved to:\n{file_path}"
                )
            except Exception as e:
                logger.error(f"Error exporting HTML: {e}")
                QMessageBox.critical(
                    self, "Export Error", f"Could not export chart:\n{e}"
                )

    def clear_chart(self) -> None:
        """Clear the current chart display."""
        if self.web_view:
            self.web_view.setHtml("")
        self.current_fig = None
        self.export_png_button.setEnabled(False)
        self.export_html_button.setEnabled(False)
        logger.debug("Chart cleared")
