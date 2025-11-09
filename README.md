# PEA ETF Tracker

A local Python application for macOS designed to simulate, track, and optimize a portfolio of ETFs eligible for the French PEA (Plan d'Épargne en Actions) account.

## Features (Version 1.0 MVP)

### Portfolio Management
- ✅ Create and manage simulated ETF portfolios
- ✅ Add, edit, and remove ETF positions (ticker, quantity, buy price, date)
- ✅ Import/export portfolios from CSV
- ✅ Track portfolio value and P&L over time

### Market Data Integration
- ✅ Auto-fetch latest prices from Yahoo Finance
- ✅ Price caching for offline use
- ✅ Manual CSV fallback option
- ✅ Historical data retrieval

### Analytics & Risk Metrics
- ✅ Portfolio performance calculations (daily, weekly, monthly returns)
- ✅ Risk metrics: volatility, Sharpe ratio, maximum drawdown
- ✅ Asset correlation analysis
- ✅ Diversification metrics

### Visualization
- ✅ Portfolio value over time (line chart)
- ✅ Asset allocation (pie and bar charts)
- ✅ Risk/return scatter plot
- ✅ Individual ETF performance charts

### User Preferences
- ✅ Persistent settings and configuration
- ✅ Default currency (EUR)
- ✅ Data source selection
- ✅ Chart preferences

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.11+ |
| UI Framework | PyQt6 |
| Data Source | Yahoo Finance (yfinance) |
| Visualization | Plotly |
| Data Processing | Pandas, NumPy |
| Persistence | JSON |
| Testing | pytest |
| Code Quality | black, pylint, mypy |

## Installation

### Prerequisites
- macOS 10.15 or later
- Python 3.11 or later

### Setup Instructions

1. **Clone the repository** (or download the source code)
   ```bash
   cd "/Users/philippe/Documents/ETF Manager"
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   python main.py
   ```

## Usage

### Running the Application

```bash
# Activate virtual environment (if not already active)
source .venv/bin/activate

# Run the application
python main.py
```

### Creating a Portfolio

1. Launch the application
2. Click **File → New Portfolio**
3. Add ETF positions using the **Add Position** button
4. Enter ticker symbol (e.g., `EWLD.PA`, `PE500.PA`)
5. Specify quantity, buy price, and purchase date
6. Click **Save**

### Importing a Portfolio from CSV

1. Click **File → Import Portfolio**
2. Select your CSV file with the following format:
   ```csv
   Ticker,Name,Quantity,BuyPrice,BuyDate
   EWLD.PA,Amundi MSCI World,100,28.50,2024-01-15
   PE500.PA,Lyxor S&P 500,50,42.30,2024-02-10
   ```
3. Review the imported data
4. Click **Confirm**

### Viewing Charts

1. Select chart type from dropdown (Portfolio Value, Allocation, Risk/Return)
2. Click **Refresh** to update with latest data
3. Export charts via **File → Export Chart**

### Configuration

User settings are stored in:
```
~/Library/Application Support/PEA_ETF_Tracker/config.json
```

## Development

### Project Structure

```
ETF Manager/
├── main.py                 # Application entry point
├── requirements.txt        # Dependencies
├── pyproject.toml         # Tool configuration
├── ui/                    # PyQt6 UI components
├── data/                  # Data management
├── analytics/             # Portfolio analytics
├── config/                # Configuration
├── visuals/               # Chart generation
├── tests/                 # Test suite
├── sample_data/           # Sample data
└── docs/                  # Documentation
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_portfolio.py
```

### Code Quality Gates

Before committing code, ensure all quality gates pass:

```bash
# Format code
black .

# Lint (score must be ≥ 8.0)
pylint ui/ data/ analytics/ config/ visuals/

# Type check
mypy .

# Run tests
pytest
```

### Development Workflow

This project follows Test-Driven Development (TDD):

1. Write failing test
2. Implement minimum code to pass test
3. Refactor and improve
4. Run quality gates
5. Commit with conventional commits format

See [AI_CODING_RULES.md](AI_CODING_RULES.md) for detailed coding standards.

## Sample Data

The `sample_data/` directory contains:
- `demo_portfolio.csv` - Example portfolio with PEA-eligible ETFs
- `demo_config.json` - Sample configuration
- `sample_etfs.json` - Common PEA-eligible ETF tickers

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Cmd+N` | New Portfolio |
| `Cmd+O` | Open Portfolio |
| `Cmd+S` | Save Portfolio |
| `Cmd+I` | Import from CSV |
| `Cmd+E` | Export to CSV |
| `Cmd+R` | Refresh Market Data |
| `Cmd+,` | Settings |
| `Cmd+Q` | Quit Application |

## Troubleshooting

### Market Data Not Updating
- Check internet connection
- Verify Yahoo Finance is accessible
- Try manual refresh (`Cmd+R`)
- Check `error.log` in application support folder

### Portfolio Won't Load
- Verify JSON file format
- Check file permissions
- Try importing from CSV instead
- Restore from backup if available

### Application Won't Start
- Verify Python version: `python --version` (must be 3.11+)
- Reinstall dependencies: `pip install -r requirements.txt`
- Check for error messages in terminal

## Configuration Files

### Application Support Location
```
~/Library/Application Support/PEA_ETF_Tracker/
├── config.json          # User settings
├── cache/              # Price cache
└── error.log           # Error logs
```

### Config.json Format
```json
{
  "default_currency": "EUR",
  "data_source": "yfinance",
  "etfs": [
    {"ticker": "EWLD.PA", "name": "Amundi MSCI World", "weight": 0.25},
    {"ticker": "PE500.PA", "name": "Lyxor S&P 500", "weight": 0.25}
  ],
  "chart_preferences": "performance",
  "last_portfolio_path": "/path/to/portfolio.csv"
}
```

## Common PEA-Eligible ETFs

| Ticker | Name | Category |
|--------|------|----------|
| EWLD.PA | Amundi MSCI World | World Equity |
| PE500.PA | Lyxor S&P 500 | US Large Cap |
| PAEEM.PA | Lyxor MSCI Emerging Markets | Emerging Markets |
| PCEU.PA | Lyxor STOXX Europe 600 | European Equity |
| PSP5.PA | Amundi MSCI Europe | European Equity |

## Roadmap

### Version 1.1 (Quality & UX)
- Auto-refresh during market hours
- Enhanced error handling
- Portfolio snapshots
- Additional chart options

### Version 2.0 (Analytics Expansion)
- Correlation matrix visualization
- Sortino ratio
- Enhanced reporting (PDF/CSV export)

### Version 3.0 (Portfolio Optimization)
- Mean-variance optimization (Markowitz)
- Rebalancing simulator
- Strategy comparison tools

## License

This project is for educational purposes.

## Contributing

See [PROJECT_PLAN.md](PROJECT_PLAN.md) for development roadmap and [AI_CODING_RULES.md](AI_CODING_RULES.md) for coding standards.

## Support

For issues and feature requests, please refer to the project documentation.

## Screenshots

_Screenshots coming soon - application fully functional_

**Main Window:**
- Portfolio table with real-time price updates
- Sortable columns (Ticker, Name, Quantity, Buy Price, Current Price, P&L, P&L %)
- Context menu for Edit/Delete positions

**Dashboard:**
- KPI cards: Total Value, Total Invested, P&L, P&L %, Positions Count
- Color-coded P&L display (green positive, red negative)
- Real-time updates on price refresh

**Charts:**
- Portfolio Value Over Time (line chart)
- Asset Allocation (pie chart, bar chart)
- Risk vs Return scatter plot
- Individual ETF performance charts
- Export to PNG/HTML

---

**Version:** 1.0.0
**Last Updated:** 2025-11-09
**Status:** v1.0 MVP Complete - Ready for Release ✅
