"""
Tests for data.portfolio module.

Tests ETF position management and portfolio CRUD operations.
"""

import csv
from datetime import date
from pathlib import Path

import pytest

from data.portfolio import ETFPosition, Portfolio


# ETFPosition tests
def test_etfposition_creation() -> None:
    """ETFPosition can be created with all required fields."""
    position = ETFPosition(
        ticker="EWLD.PA",
        name="Amundi MSCI World UCITS ETF",
        quantity=100.0,
        buy_price=28.50,
        buy_date=date(2024, 1, 15),
    )

    assert position.ticker == "EWLD.PA"
    assert position.name == "Amundi MSCI World UCITS ETF"
    assert position.quantity == 100.0
    assert position.buy_price == 28.50
    assert position.buy_date == date(2024, 1, 15)


def test_etfposition_to_dict() -> None:
    """ETFPosition.to_dict() returns correct dictionary."""
    position = ETFPosition(
        ticker="PE500.PA",
        name="Lyxor S&P 500",
        quantity=50.0,
        buy_price=42.30,
        buy_date=date(2024, 2, 10),
    )

    result = position.to_dict()

    assert result["ticker"] == "PE500.PA"
    assert result["name"] == "Lyxor S&P 500"
    assert result["quantity"] == 50.0
    assert result["buy_price"] == 42.30
    assert result["buy_date"] == "2024-02-10"


def test_etfposition_from_dict() -> None:
    """ETFPosition.from_dict() reconstructs object correctly."""
    data = {
        "ticker": "PAEEM.PA",
        "name": "Lyxor Emergents",
        "quantity": 75.0,
        "buy_price": 18.25,
        "buy_date": "2024-03-05",
    }

    position = ETFPosition.from_dict(data)

    assert position.ticker == "PAEEM.PA"
    assert position.name == "Lyxor Emergents"
    assert position.quantity == 75.0
    assert position.buy_price == 18.25
    assert position.buy_date == date(2024, 3, 5)


# Portfolio CRUD tests
def test_portfolio_empty_initialization() -> None:
    """Portfolio can be initialized empty."""
    portfolio = Portfolio()

    assert len(portfolio.positions) == 0


def test_portfolio_initialization_with_positions() -> None:
    """Portfolio can be initialized with existing positions."""
    positions = [
        ETFPosition("EWLD.PA", "Amundi World", 100.0, 28.50, date(2024, 1, 15)),
        ETFPosition("PE500.PA", "Lyxor S&P 500", 50.0, 42.30, date(2024, 2, 10)),
    ]

    portfolio = Portfolio(positions)

    assert len(portfolio.positions) == 2


def test_portfolio_add_position() -> None:
    """Portfolio.add_position() adds position to portfolio."""
    portfolio = Portfolio()
    position = ETFPosition("EWLD.PA", "Amundi World", 100.0, 28.50, date(2024, 1, 15))

    portfolio.add_position(position)

    assert len(portfolio.positions) == 1
    assert portfolio.positions[0].ticker == "EWLD.PA"


def test_portfolio_add_duplicate_raises_error() -> None:
    """Adding duplicate ticker raises ValueError."""
    portfolio = Portfolio()
    position1 = ETFPosition("EWLD.PA", "Amundi World", 100.0, 28.50, date(2024, 1, 15))
    position2 = ETFPosition("EWLD.PA", "Amundi World", 200.0, 29.00, date(2024, 2, 15))

    portfolio.add_position(position1)

    with pytest.raises(ValueError, match="already exists"):
        portfolio.add_position(position2)


def test_portfolio_remove_position() -> None:
    """Portfolio.remove_position() removes position."""
    position = ETFPosition("EWLD.PA", "Amundi World", 100.0, 28.50, date(2024, 1, 15))
    portfolio = Portfolio([position])

    portfolio.remove_position("EWLD.PA")

    assert len(portfolio.positions) == 0


def test_portfolio_remove_nonexistent_raises_error() -> None:
    """Removing non-existent ticker raises ValueError."""
    portfolio = Portfolio()

    with pytest.raises(ValueError, match="not found"):
        portfolio.remove_position("NONEXISTENT.PA")


def test_portfolio_update_position() -> None:
    """Portfolio.update_position() updates existing position."""
    position = ETFPosition("EWLD.PA", "Amundi World", 100.0, 28.50, date(2024, 1, 15))
    portfolio = Portfolio([position])

    new_position = ETFPosition(
        "EWLD.PA", "Amundi World Updated", 200.0, 29.00, date(2024, 2, 15)
    )
    portfolio.update_position("EWLD.PA", new_position)

    assert len(portfolio.positions) == 1
    assert portfolio.positions[0].quantity == 200.0
    assert portfolio.positions[0].buy_price == 29.00


def test_portfolio_update_nonexistent_raises_error() -> None:
    """Updating non-existent ticker raises ValueError."""
    portfolio = Portfolio()
    position = ETFPosition("EWLD.PA", "Amundi World", 100.0, 28.50, date(2024, 1, 15))

    with pytest.raises(ValueError, match="not found"):
        portfolio.update_position("NONEXISTENT.PA", position)


def test_portfolio_get_position() -> None:
    """Portfolio.get_position() returns correct position."""
    position = ETFPosition("EWLD.PA", "Amundi World", 100.0, 28.50, date(2024, 1, 15))
    portfolio = Portfolio([position])

    result = portfolio.get_position("EWLD.PA")

    assert result is not None
    assert result.ticker == "EWLD.PA"
    assert result.quantity == 100.0


def test_portfolio_get_nonexistent_position() -> None:
    """Portfolio.get_position() returns None for non-existent ticker."""
    portfolio = Portfolio()

    result = portfolio.get_position("NONEXISTENT.PA")

    assert result is None


def test_portfolio_get_all_positions() -> None:
    """Portfolio.get_all_positions() returns all positions."""
    positions = [
        ETFPosition("EWLD.PA", "Amundi World", 100.0, 28.50, date(2024, 1, 15)),
        ETFPosition("PE500.PA", "Lyxor S&P 500", 50.0, 42.30, date(2024, 2, 10)),
    ]
    portfolio = Portfolio(positions)

    result = portfolio.get_all_positions()

    assert len(result) == 2
    assert result[0].ticker == "EWLD.PA"
    assert result[1].ticker == "PE500.PA"


# JSON persistence tests
def test_save_and_load_json_preserves_data(tmp_path: Path) -> None:
    """Portfolio saved to JSON and loaded back is identical."""
    positions = [
        ETFPosition("EWLD.PA", "Amundi World", 100.0, 28.50, date(2024, 1, 15)),
        ETFPosition("PE500.PA", "Lyxor S&P 500", 50.0, 42.30, date(2024, 2, 10)),
    ]
    portfolio = Portfolio(positions)

    json_file = tmp_path / "portfolio.json"
    portfolio.save_to_json(json_file)

    loaded_portfolio = Portfolio.load_from_json(json_file)

    assert len(loaded_portfolio.positions) == 2
    assert loaded_portfolio.positions[0].ticker == "EWLD.PA"
    assert loaded_portfolio.positions[0].buy_date == date(2024, 1, 15)
    assert loaded_portfolio.positions[1].ticker == "PE500.PA"


def test_load_json_with_missing_file_raises_error(tmp_path: Path) -> None:
    """Loading missing JSON file raises FileNotFoundError."""
    json_file = tmp_path / "nonexistent.json"

    with pytest.raises(FileNotFoundError):
        Portfolio.load_from_json(json_file)


# CSV import/export tests
def test_export_csv_creates_valid_file(tmp_path: Path) -> None:
    """export_to_csv() creates CSV with correct format."""
    positions = [
        ETFPosition("EWLD.PA", "Amundi World", 100.0, 28.50, date(2024, 1, 15)),
        ETFPosition("PE500.PA", "Lyxor S&P 500", 50.0, 42.30, date(2024, 2, 10)),
    ]
    portfolio = Portfolio(positions)

    csv_file = tmp_path / "portfolio.csv"
    portfolio.export_to_csv(csv_file)

    assert csv_file.exists()

    # Verify CSV format
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == [
            "Ticker",
            "Name",
            "Quantity",
            "BuyPrice",
            "BuyDate",
            "ManualPrice",
        ]

        row1 = next(reader)
        assert row1[0] == "EWLD.PA"
        assert row1[4] == "2024-01-15"
        assert row1[5] == ""  # No manual price


def test_import_csv_loads_positions_correctly(tmp_path: Path) -> None:
    """import_from_csv() loads demo_portfolio.csv correctly."""
    csv_file = tmp_path / "portfolio.csv"

    # Create test CSV
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Ticker", "Name", "Quantity", "BuyPrice", "BuyDate"])
        writer.writerow(["EWLD.PA", "Amundi World", "100.0", "28.50", "2024-01-15"])
        writer.writerow(["PE500.PA", "Lyxor S&P 500", "50.0", "42.30", "2024-02-10"])

    portfolio = Portfolio.import_from_csv(csv_file)

    assert len(portfolio.positions) == 2
    assert portfolio.positions[0].ticker == "EWLD.PA"
    assert portfolio.positions[0].quantity == 100.0
    assert portfolio.positions[0].buy_date == date(2024, 1, 15)


def test_import_csv_with_invalid_format_raises_error(tmp_path: Path) -> None:
    """Importing invalid CSV raises ValueError."""
    csv_file = tmp_path / "invalid.csv"

    # Create CSV with wrong headers
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Wrong", "Headers"])
        writer.writerow(["EWLD.PA", "100"])

    with pytest.raises(ValueError, match="missing required columns"):
        Portfolio.import_from_csv(csv_file)


@pytest.mark.parametrize(
    "invalid_date",
    ["2024-13-01", "not-a-date", ""],
)
def test_import_csv_with_invalid_date_raises_error(
    tmp_path: Path, invalid_date: str
) -> None:
    """Importing CSV with invalid date raises ValueError."""
    csv_file = tmp_path / "invalid_date.csv"

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Ticker", "Name", "Quantity", "BuyPrice", "BuyDate"])
        writer.writerow(["EWLD.PA", "Amundi World", "100.0", "28.50", invalid_date])

    with pytest.raises(ValueError):
        Portfolio.import_from_csv(csv_file)


def test_import_actual_demo_portfolio() -> None:
    """Import the actual demo_portfolio.csv file."""
    demo_file = Path("sample_data/demo_portfolio.csv")

    if demo_file.exists():
        portfolio = Portfolio.import_from_csv(demo_file)

        assert len(portfolio.positions) == 5
        assert portfolio.positions[0].ticker == "EWLD.PA"
        assert portfolio.positions[0].quantity == 100.0


# Manual Price Override tests (Phase 1)
def test_etfposition_with_manual_price() -> None:
    """ETFPosition can be created with manual price override."""
    position = ETFPosition(
        ticker="EWLD.PA",
        name="Amundi World",
        quantity=100.0,
        buy_price=28.50,
        buy_date=date(2024, 1, 15),
        manual_price=30.00,
    )

    assert position.manual_price == 30.00


def test_etfposition_without_manual_price() -> None:
    """ETFPosition manual_price defaults to None."""
    position = ETFPosition(
        ticker="EWLD.PA",
        name="Amundi World",
        quantity=100.0,
        buy_price=28.50,
        buy_date=date(2024, 1, 15),
    )

    assert position.manual_price is None


def test_etfposition_to_dict_with_manual_price() -> None:
    """ETFPosition.to_dict() includes manual_price when set."""
    position = ETFPosition(
        ticker="PE500.PA",
        name="Lyxor S&P 500",
        quantity=50.0,
        buy_price=42.30,
        buy_date=date(2024, 2, 10),
        manual_price=45.00,
    )

    result = position.to_dict()

    assert result["manual_price"] == 45.00


def test_etfposition_to_dict_without_manual_price() -> None:
    """ETFPosition.to_dict() includes manual_price as None when not set."""
    position = ETFPosition(
        ticker="PE500.PA",
        name="Lyxor S&P 500",
        quantity=50.0,
        buy_price=42.30,
        buy_date=date(2024, 2, 10),
    )

    result = position.to_dict()

    assert result["manual_price"] is None


def test_etfposition_from_dict_with_manual_price() -> None:
    """ETFPosition.from_dict() reconstructs manual_price correctly."""
    data = {
        "ticker": "PAEEM.PA",
        "name": "Lyxor Emergents",
        "quantity": 75.0,
        "buy_price": 18.25,
        "buy_date": "2024-03-05",
        "manual_price": 20.00,
    }

    position = ETFPosition.from_dict(data)

    assert position.manual_price == 20.00


def test_etfposition_from_dict_backward_compatible() -> None:
    """ETFPosition.from_dict() handles missing manual_price (backward compatibility)."""
    data = {
        "ticker": "PAEEM.PA",
        "name": "Lyxor Emergents",
        "quantity": 75.0,
        "buy_price": 18.25,
        "buy_date": "2024-03-05",
    }

    position = ETFPosition.from_dict(data)

    assert position.manual_price is None


def test_portfolio_export_csv_with_manual_price(tmp_path: Path) -> None:
    """export_to_csv() includes ManualPrice column."""
    positions = [
        ETFPosition(
            "EWLD.PA",
            "Amundi World",
            100.0,
            28.50,
            date(2024, 1, 15),
            manual_price=30.00,
        ),
        ETFPosition("PE500.PA", "Lyxor S&P 500", 50.0, 42.30, date(2024, 2, 10)),
    ]
    portfolio = Portfolio(positions)

    csv_file = tmp_path / "portfolio.csv"
    portfolio.export_to_csv(csv_file)

    # Verify CSV format includes ManualPrice column
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        assert "ManualPrice" in header

        row1 = next(reader)
        manual_price_idx = header.index("ManualPrice")
        assert row1[manual_price_idx] == "30.0"

        row2 = next(reader)
        assert row2[manual_price_idx] == ""


def test_portfolio_import_csv_with_manual_price(tmp_path: Path) -> None:
    """import_from_csv() loads manual prices correctly."""
    csv_file = tmp_path / "portfolio.csv"

    # Create test CSV with ManualPrice column
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["Ticker", "Name", "Quantity", "BuyPrice", "BuyDate", "ManualPrice"]
        )
        writer.writerow(
            ["EWLD.PA", "Amundi World", "100.0", "28.50", "2024-01-15", "30.00"]
        )
        writer.writerow(
            ["PE500.PA", "Lyxor S&P 500", "50.0", "42.30", "2024-02-10", ""]
        )

    portfolio = Portfolio.import_from_csv(csv_file)

    assert len(portfolio.positions) == 2
    assert portfolio.positions[0].manual_price == 30.00
    assert portfolio.positions[1].manual_price is None


def test_portfolio_import_csv_backward_compatible(tmp_path: Path) -> None:
    """import_from_csv() handles old CSV without ManualPrice column."""
    csv_file = tmp_path / "portfolio_old.csv"

    # Create old format CSV without ManualPrice
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Ticker", "Name", "Quantity", "BuyPrice", "BuyDate"])
        writer.writerow(["EWLD.PA", "Amundi World", "100.0", "28.50", "2024-01-15"])

    portfolio = Portfolio.import_from_csv(csv_file)

    assert len(portfolio.positions) == 1
    assert portfolio.positions[0].manual_price is None
