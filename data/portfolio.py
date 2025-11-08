"""
Portfolio data models for PEA ETF Tracker.

Manages ETF positions and portfolio persistence (JSON and CSV).
"""

import csv
import json
import logging
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class ETFPosition:
    """
    Represents a single ETF position in the portfolio.

    Attributes:
        ticker: ETF ticker symbol (e.g., "EWLD.PA")
        name: ETF name (e.g., "Amundi MSCI World UCITS ETF")
        quantity: Number of shares owned (supports fractional shares)
        buy_price: Purchase price per share in EUR
        buy_date: Date of purchase

    Example:
        >>> position = ETFPosition(
        ...     ticker="EWLD.PA",
        ...     name="Amundi MSCI World",
        ...     quantity=100.0,
        ...     buy_price=28.50,
        ...     buy_date=date(2024, 1, 15)
        ... )
    """

    ticker: str
    name: str
    quantity: float
    buy_price: float
    buy_date: date

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to JSON-serializable dictionary.

        Returns:
            Dictionary with all position data, date as ISO string.

        Example:
            >>> position.to_dict()
            {'ticker': 'EWLD.PA', ..., 'buy_date': '2024-01-15'}
        """
        return {
            "ticker": self.ticker,
            "name": self.name,
            "quantity": self.quantity,
            "buy_price": self.buy_price,
            "buy_date": self.buy_date.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ETFPosition":
        """
        Create ETFPosition from dictionary (for JSON deserialization).

        Args:
            data: Dictionary with position data.

        Returns:
            ETFPosition object.

        Raises:
            KeyError: If required keys are missing.
            ValueError: If date format is invalid.

        Example:
            >>> data = {'ticker': 'EWLD.PA', ..., 'buy_date': '2024-01-15'}
            >>> position = ETFPosition.from_dict(data)
        """
        return cls(
            ticker=data["ticker"],
            name=data["name"],
            quantity=float(data["quantity"]),
            buy_price=float(data["buy_price"]),
            buy_date=date.fromisoformat(data["buy_date"]),
        )


class Portfolio:
    """
    Manages a collection of ETF positions.

    Provides CRUD operations and persistence (JSON/CSV).

    Example:
        >>> portfolio = Portfolio()
        >>> position = ETFPosition("EWLD.PA", "Amundi World", 100, 28.5, date.today())
        >>> portfolio.add_position(position)
        >>> portfolio.save_to_json(Path("portfolio.json"))
    """

    def __init__(self, positions: Optional[List[ETFPosition]] = None) -> None:
        """
        Initialize portfolio with optional positions list.

        Args:
            positions: Optional list of ETFPosition objects.
        """
        self.positions: List[ETFPosition] = positions if positions is not None else []

    def add_position(self, position: ETFPosition) -> None:
        """
        Add a new position to the portfolio.

        Args:
            position: ETFPosition to add.

        Raises:
            ValueError: If ticker already exists in portfolio.

        Example:
            >>> portfolio.add_position(position)
        """
        # Check if ticker already exists
        if any(p.ticker == position.ticker for p in self.positions):
            raise ValueError(f"Ticker {position.ticker} already exists in portfolio")

        self.positions.append(position)
        logger.info(f"Added position: {position.ticker}")

    def remove_position(self, ticker: str) -> None:
        """
        Remove position by ticker symbol.

        Args:
            ticker: Ticker symbol to remove.

        Raises:
            ValueError: If ticker not found in portfolio.

        Example:
            >>> portfolio.remove_position("EWLD.PA")
        """
        for i, position in enumerate(self.positions):
            if position.ticker == ticker:
                self.positions.pop(i)
                logger.info(f"Removed position: {ticker}")
                return

        raise ValueError(f"Ticker {ticker} not found in portfolio")

    def update_position(self, ticker: str, new_position: ETFPosition) -> None:
        """
        Update existing position.

        Args:
            ticker: Ticker symbol to update.
            new_position: New ETFPosition data.

        Raises:
            ValueError: If ticker not found in portfolio.

        Example:
            >>> portfolio.update_position("EWLD.PA", new_position)
        """
        for i, position in enumerate(self.positions):
            if position.ticker == ticker:
                self.positions[i] = new_position
                logger.info(f"Updated position: {ticker}")
                return

        raise ValueError(f"Ticker {ticker} not found in portfolio")

    def get_position(self, ticker: str) -> Optional[ETFPosition]:
        """
        Get position by ticker symbol.

        Args:
            ticker: Ticker symbol to find.

        Returns:
            ETFPosition if found, None otherwise.

        Example:
            >>> position = portfolio.get_position("EWLD.PA")
        """
        for position in self.positions:
            if position.ticker == ticker:
                return position
        return None

    def get_all_positions(self) -> List[ETFPosition]:
        """
        Get all positions in portfolio.

        Returns:
            List of all ETFPosition objects.

        Example:
            >>> positions = portfolio.get_all_positions()
        """
        return self.positions.copy()

    def save_to_json(self, path: Path) -> None:
        """
        Save portfolio to JSON file.

        Args:
            path: Path to JSON file.

        Raises:
            OSError: If unable to write file.

        Example:
            >>> portfolio.save_to_json(Path("portfolio.json"))
        """
        data = {"positions": [position.to_dict() for position in self.positions]}

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        logger.info(f"Portfolio saved to {path}")

    @classmethod
    def load_from_json(cls, path: Path) -> "Portfolio":
        """
        Load portfolio from JSON file.

        Args:
            path: Path to JSON file.

        Returns:
            Portfolio object.

        Raises:
            FileNotFoundError: If file doesn't exist.
            json.JSONDecodeError: If JSON is invalid.
            KeyError: If required fields are missing.

        Example:
            >>> portfolio = Portfolio.load_from_json(Path("portfolio.json"))
        """
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        positions = [ETFPosition.from_dict(pos_data) for pos_data in data["positions"]]

        logger.info(f"Portfolio loaded from {path}")
        return cls(positions)

    def export_to_csv(self, path: Path) -> None:
        """
        Export portfolio to CSV file.

        CSV format: Ticker,Name,Quantity,BuyPrice,BuyDate

        Args:
            path: Path to CSV file.

        Raises:
            OSError: If unable to write file.

        Example:
            >>> portfolio.export_to_csv(Path("portfolio.csv"))
        """
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Ticker", "Name", "Quantity", "BuyPrice", "BuyDate"])

            for position in self.positions:
                writer.writerow(
                    [
                        position.ticker,
                        position.name,
                        position.quantity,
                        position.buy_price,
                        position.buy_date.isoformat(),
                    ]
                )

        logger.info(f"Portfolio exported to {path}")

    @classmethod
    def import_from_csv(cls, path: Path) -> "Portfolio":
        """
        Import portfolio from CSV file.

        Expected CSV format:
        Ticker,Name,Quantity,BuyPrice,BuyDate
        EWLD.PA,Amundi MSCI World UCITS ETF,100,28.50,2024-01-15

        Args:
            path: Path to CSV file.

        Returns:
            Portfolio object with imported positions.

        Raises:
            FileNotFoundError: If CSV file doesn't exist.
            ValueError: If CSV format is invalid or missing required columns.

        Example:
            >>> portfolio = Portfolio.import_from_csv(Path("demo_portfolio.csv"))
        """
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            # Verify required columns
            required_columns = {"Ticker", "Name", "Quantity", "BuyPrice", "BuyDate"}
            if reader.fieldnames is None or not required_columns.issubset(
                set(reader.fieldnames)
            ):
                raise ValueError(
                    f"CSV file missing required columns. "
                    f"Expected: {required_columns}, "
                    f"Found: {reader.fieldnames}"
                )

            positions = []
            for row in reader:
                try:
                    position = ETFPosition(
                        ticker=row["Ticker"],
                        name=row["Name"],
                        quantity=float(row["Quantity"]),
                        buy_price=float(row["BuyPrice"]),
                        buy_date=date.fromisoformat(row["BuyDate"]),
                    )
                    positions.append(position)
                except (ValueError, KeyError) as e:
                    raise ValueError(
                        f"Invalid data in CSV row: {row}. Error: {e}"
                    ) from e

        logger.info(f"Portfolio imported from {path} with {len(positions)} positions")
        return cls(positions)
