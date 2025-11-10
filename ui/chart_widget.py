"""
Chart widget for displaying Plotly charts.

Provides a widget for displaying interactive Plotly charts using QWebEngineView.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6.QtCore import Qt, pyqtSignal
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

from config.settings import ChartPreferences

logger = logging.getLogger(__name__)


class ChartWidget(QWidget):
    """Widget for displaying matplotlib charts."""

    # Signal emitted when chart type selection changes
    chart_type_changed = pyqtSignal(str)

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
        self.current_figure: Optional[Figure] = None
        self.current_tickers: List[str] = []
        self.current_percentages: List[float] = []
        self.current_values: Dict[str, float] = {}  # For bar chart
        self._setup_ui()
        logger.debug("Chart widget initialized")

    def _setup_ui(self) -> None:
        """Create UI elements."""
        layout = QVBoxLayout()

        # Top controls
        controls_layout = QHBoxLayout()

        # Chart type selector (only show available charts)
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(
            [
                "Allocation Pie",
                "Allocation Bar",
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

        # Matplotlib canvas for native chart display
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setMinimumHeight(400)
        layout.addWidget(self.canvas)

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
        logger.debug("Chart type changed to: %s", chart_type)
        # Emit signal to notify main window
        self.chart_type_changed.emit(chart_type)

    def display_chart(
        self,
        chart_type: str,
        tickers: List[str],
        percentages: Optional[List[float]] = None,
        values: Optional[Dict[str, float]] = None,
    ) -> None:
        """
        Display chart based on type.

        Args:
            chart_type: Chart type - "Allocation Pie" or "Allocation Bar".
            tickers: List of ticker symbols.
            percentages: List of allocation percentages (0-100) for pie chart.
            values: Dict mapping ticker to value (EUR) for bar chart.

        Example:
            >>> widget.display_chart("Allocation Pie", ["VT", "IWDA"], [60.5, 39.5])
            >>> widget.display_chart("Allocation Bar", ["VT", "IWDA"], values={"VT": 6000, "IWDA": 4000})
        """
        # Store current data for export
        self.current_tickers = tickers
        if percentages:
            self.current_percentages = percentages
        if values:
            self.current_values = values

        # Clear previous figure
        self.figure.clear()

        if chart_type == "Allocation Pie":
            self._render_pie_chart(tickers, percentages or [])
        elif chart_type == "Allocation Bar":
            self._render_bar_chart(tickers, values or {})
        else:
            logger.warning("Unknown chart type: %s", chart_type)
            return

        # Adjust layout to prevent label cutoff
        self.figure.tight_layout()

        # Redraw canvas
        self.canvas.draw()

        # Enable export buttons
        self.export_png_button.setEnabled(True)
        self.export_html_button.setEnabled(
            False
        )  # HTML export not supported with matplotlib

        logger.info("Chart displayed: %s with %d positions", chart_type, len(tickers))

    def _render_pie_chart(self, tickers: List[str], percentages: List[float]) -> None:
        """
        Render pie chart with allocation percentages.

        Args:
            tickers: List of ticker symbols.
            percentages: List of allocation percentages (0-100).
        """
        ax = self.figure.add_subplot(111)
        colors = plt.cm.Set3(range(len(tickers)))  # type: ignore[attr-defined]

        wedges, texts, autotexts = ax.pie(  # type: ignore[misc]
            percentages,
            labels=tickers,
            autopct="%1.1f%%",
            startangle=90,
            colors=colors,
            textprops={"fontsize": 10},
        )

        # Make percentage text bold and white
        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontweight("bold")

        ax.set_title("Portfolio Allocation", fontsize=14, fontweight="bold", pad=20)

        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis("equal")

    def _render_bar_chart(self, tickers: List[str], values: Dict[str, float]) -> None:
        """
        Render bar chart with position values.

        Args:
            tickers: List of ticker symbols.
            values: Dict mapping ticker to value (EUR).
        """
        ax = self.figure.add_subplot(111)

        # Extract values in same order as tickers
        bar_values = [values.get(ticker, 0.0) for ticker in tickers]

        # Create bar chart
        bars = ax.bar(
            tickers,
            bar_values,
            color=plt.cm.Set3(range(len(tickers))),  # type: ignore[attr-defined]
            edgecolor="black",
        )

        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"€{height:,.0f}",
                ha="center",
                va="bottom",
                fontsize=9,
            )

        ax.set_title("Position Values", fontsize=14, fontweight="bold", pad=20)
        ax.set_xlabel("Ticker", fontsize=11)
        ax.set_ylabel("Value (EUR)", fontsize=11)
        ax.grid(axis="y", alpha=0.3)

        # Rotate x-axis labels if many tickers
        if len(tickers) > 5:
            ax.set_xticklabels(tickers, rotation=45, ha="right")

    def _export_png(self) -> None:
        """Export current chart to PNG file."""
        if not self.current_tickers:
            QMessageBox.warning(self, "Export Error", "No chart to export")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Chart as PNG", "", "PNG Files (*.png)"
        )

        if file_path:
            try:
                self.figure.savefig(file_path, dpi=300, bbox_inches="tight")
                logger.info("Chart exported to PNG: %s", file_path)
                QMessageBox.information(
                    self, "Export Successful", f"Chart saved to:\n{file_path}"
                )
            except Exception as e:
                logger.error("Error exporting PNG: %s", e)
                QMessageBox.critical(
                    self, "Export Error", f"Could not export chart:\n{e}"
                )

    def _export_html(self) -> None:
        """Export current chart to HTML file (not supported with matplotlib)."""
        QMessageBox.information(
            self,
            "Export Not Supported",
            "HTML export is not available with the native chart display.\n\n"
            "Please use PNG export instead.",
        )

    def clear_chart(self) -> None:
        """Clear the current chart display."""
        self.figure.clear()
        self.canvas.draw()
        self.current_tickers = []
        self.current_percentages = []
        self.export_png_button.setEnabled(False)
        self.export_html_button.setEnabled(False)
        logger.debug("Chart cleared")

    def show_empty_state(self) -> None:
        """Show empty state message when no data is available."""
        self.figure.clear()

        # Add centered text message
        ax = self.figure.add_subplot(111)
        ax.text(
            0.5,
            0.5,
            "No data to display\n\nAdd positions or refresh prices to view charts",
            horizontalalignment="center",
            verticalalignment="center",
            transform=ax.transAxes,
            fontsize=12,
            color="#666",
        )
        ax.axis("off")

        self.canvas.draw()

        self.current_tickers = []
        self.current_percentages = []
        self.export_png_button.setEnabled(False)
        self.export_html_button.setEnabled(False)
        logger.debug("Empty state displayed")
