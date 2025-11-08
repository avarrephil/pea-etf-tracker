"""
Tests for config.settings module.

Tests configuration management including loading, saving,
and fallback to defaults.
"""

import json
from pathlib import Path

import pytest

from config.settings import (
    ChartPreferences,
    ETFInfo,
    Settings,
    WindowGeometry,
    get_default_settings,
    load_settings,
    save_settings,
)


def test_get_default_settings_returns_valid_settings() -> None:
    """get_default_settings() returns Settings with all required fields."""
    settings = get_default_settings()

    assert isinstance(settings, Settings)
    assert settings.default_currency == "EUR"
    assert settings.data_source == "yfinance"
    assert isinstance(settings.chart_preferences, ChartPreferences)
    assert isinstance(settings.window_geometry, WindowGeometry)
    assert isinstance(settings.etfs, list)


def test_chart_preferences_has_correct_defaults() -> None:
    """ChartPreferences dataclass has sensible defaults."""
    prefs = ChartPreferences(
        default_chart="portfolio_value",
        color_scheme="plotly",
        show_grid=True,
        show_legend=True,
    )

    assert prefs.default_chart == "portfolio_value"
    assert prefs.color_scheme == "plotly"
    assert prefs.show_grid is True
    assert prefs.show_legend is True


def test_window_geometry_has_correct_defaults() -> None:
    """WindowGeometry dataclass has sensible defaults."""
    geometry = WindowGeometry(width=1200, height=800, x=100, y=100)

    assert geometry.width == 1200
    assert geometry.height == 800
    assert geometry.x == 100
    assert geometry.y == 100


def test_etf_info_can_be_created() -> None:
    """ETFInfo dataclass can be created with required fields."""
    etf = ETFInfo(ticker="EWLD.PA", name="Amundi MSCI World", weight=0.30)

    assert etf.ticker == "EWLD.PA"
    assert etf.name == "Amundi MSCI World"
    assert etf.weight == 0.30


def test_load_settings_creates_directory_if_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """load_settings() creates config directory if it doesn't exist."""
    config_dir = tmp_path / "config_test"
    config_file = config_dir / "config.json"

    monkeypatch.setattr("config.settings.CONFIG_DIR", config_dir)
    monkeypatch.setattr("config.settings.CONFIG_FILE", config_file)

    settings = load_settings()

    assert config_dir.exists()
    assert isinstance(settings, Settings)


def test_load_settings_returns_defaults_when_file_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """load_settings() returns defaults when config file doesn't exist."""
    config_dir = tmp_path / "config_test"
    config_file = config_dir / "config.json"

    monkeypatch.setattr("config.settings.CONFIG_DIR", config_dir)
    monkeypatch.setattr("config.settings.CONFIG_FILE", config_file)

    settings = load_settings()

    assert isinstance(settings, Settings)
    assert settings.default_currency == "EUR"


def test_load_settings_returns_defaults_when_file_corrupted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """load_settings() returns defaults when JSON is invalid."""
    config_dir = tmp_path / "config_test"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / "config.json"

    # Write invalid JSON
    with open(config_file, "w") as f:
        f.write("{invalid json content")

    monkeypatch.setattr("config.settings.CONFIG_DIR", config_dir)
    monkeypatch.setattr("config.settings.CONFIG_FILE", config_file)

    settings = load_settings()

    assert isinstance(settings, Settings)
    assert settings.default_currency == "EUR"


def test_save_settings_creates_valid_json(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """save_settings() writes valid JSON that can be loaded."""
    config_dir = tmp_path / "config_test"
    config_file = config_dir / "config.json"

    monkeypatch.setattr("config.settings.CONFIG_DIR", config_dir)
    monkeypatch.setattr("config.settings.CONFIG_FILE", config_file)

    settings = get_default_settings()
    save_settings(settings)

    assert config_file.exists()

    # Verify JSON is valid
    with open(config_file, "r") as f:
        data = json.load(f)
        assert "default_currency" in data
        assert "data_source" in data


def test_load_then_save_preserves_data(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Settings loaded and saved remain identical."""
    config_dir = tmp_path / "config_test"
    config_file = config_dir / "config.json"

    monkeypatch.setattr("config.settings.CONFIG_DIR", config_dir)
    monkeypatch.setattr("config.settings.CONFIG_FILE", config_file)

    # Create and save settings
    original_settings = get_default_settings()
    original_settings.default_currency = "USD"
    original_settings.auto_refresh_enabled = True
    save_settings(original_settings)

    # Load and compare
    loaded_settings = load_settings()
    assert loaded_settings.default_currency == "USD"
    assert loaded_settings.auto_refresh_enabled is True


def test_save_settings_creates_directory_if_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """save_settings() creates config directory if it doesn't exist."""
    config_dir = tmp_path / "config_test"
    config_file = config_dir / "config.json"

    monkeypatch.setattr("config.settings.CONFIG_DIR", config_dir)
    monkeypatch.setattr("config.settings.CONFIG_FILE", config_file)

    settings = get_default_settings()
    save_settings(settings)

    assert config_dir.exists()
    assert config_file.exists()


@pytest.mark.parametrize(
    "currency",
    ["EUR", "USD", "GBP"],
)
def test_settings_supports_different_currencies(currency: str) -> None:
    """Settings dataclass supports different currency values."""
    settings = get_default_settings()
    settings.default_currency = currency

    assert settings.default_currency == currency


def test_load_settings_with_type_error_uses_defaults(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """load_settings() returns defaults when config has wrong types."""
    config_dir = tmp_path / "config_test"
    config_file = config_dir / "config.json"

    monkeypatch.setattr("config.settings.CONFIG_DIR", config_dir)
    monkeypatch.setattr("config.settings.CONFIG_FILE", config_file)

    # Create config with wrong types (list instead of dict)
    config_dir.mkdir(parents=True, exist_ok=True)
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump([], f)

    settings = load_settings()

    # Should return defaults
    assert settings.default_currency == "EUR"


def test_save_settings_with_permission_error_raises(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """save_settings() raises PermissionError when directory not writable."""
    config_dir = tmp_path / "readonly_config"
    config_file = config_dir / "config.json"

    monkeypatch.setattr("config.settings.CONFIG_DIR", config_dir)
    monkeypatch.setattr("config.settings.CONFIG_FILE", config_file)

    # Create read-only directory
    config_dir.mkdir(parents=True, exist_ok=True)
    import os

    os.chmod(config_dir, 0o444)

    settings = get_default_settings()

    try:
        with pytest.raises((PermissionError, OSError)):
            save_settings(settings)
    finally:
        # Restore write permissions for cleanup
        os.chmod(config_dir, 0o755)
