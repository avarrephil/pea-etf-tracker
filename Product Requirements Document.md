# PEA ETF Tracker - Product Requirements Document (PRD)

## 1. Overview

The **PEA ETF Tracker** is a local Python application built for macOS, designed to help users simulate, track, and optimize a portfolio of ETFs eligible for the French PEA account. The goal is to provide an educational and intuitive platform with a graphical interface, free data sources, and local data persistence.

---

## 2. Objectives

- **Educate** users on portfolio management principles (allocation, diversification, performance, and risk).
- **Simulate** the performance of ETFs eligible for the PEA account.
- **Visualize** key performance indicators, allocation breakdowns, and historical data.
- **Optimize** portfolio structure based on simple metrics (risk-return, diversification).

---

## 3. Technical Stack

| Component | Technology |
|------------|-------------|
| **Programming Language** | Python 3.11+ |
| **UI Framework** | PyQt6 |
| **Data Sources** | Yahoo Finance (via `yfinance`), Euronext, or alternative free APIs |
| **Data Persistence** | Local JSON or SQLite database |
| **Visualization** | Matplotlib / Plotly (static for v1) |
| **Packaging** | PyInstaller for macOS |

---

## 4. Key Features

### 4.1 Portfolio Management
- Create and manage a simulated ETF portfolio.
- Add, edit, or remove ETF positions (ticker, name, quantity, buy price, date).
- Import/export portfolio from CSV.
- Calculate and display performance metrics (daily, weekly, monthly).
- Track total portfolio value and P&L over time.

### 4.2 Market Data Integration
- Auto-fetch latest market prices for selected ETFs.
- Fallback option to update prices manually via CSV.
- Display daily close, variation %, and charted performance.

### 4.3 Visualization
- Static charts (Matplotlib/Plotly):
  - Portfolio value over time.
  - Asset allocation by sector/geography.
  - Risk/return scatter plot.
- Interactive elements (PyQt6 buttons and dropdowns for chart selection).

### 4.4 Risk Control & Analytics
- Compute portfolio volatility and Sharpe ratio.
- Calculate asset correlations.
- Display maximum drawdown and diversification metrics.

### 4.5 Portfolio Optimization (Phase 2)
- Implement mean-variance optimization (Markowitz framework).
- Allow user to simulate rebalancing scenarios.

### 4.6 User Preferences Persistence
- Save and load user settings automatically.
- Persist:
  - Preferred currency (EUR default)
  - Default data source (Yahoo Finance, Euronext API, or CSV)
  - Default ETFs list (with tickers and weights)
  - Chart preferences (e.g., performance vs allocation)
  - Last opened portfolio file path
- Storage method:
  - JSON configuration file located under `~/Library/Application Support/PEA_ETF_Tracker/config.json`
  - Example:

```json
{
  "default_currency": "EUR",
  "data_source": "yfinance",
  "etfs": [
    {"ticker": "EWLD.PA", "name": "Amundi MSCI World", "weight": 0.25},
    {"ticker": "PE500.PA", "name": "Lyxor S&P 500", "weight": 0.25}
  ],
  "chart_preferences": "performance",
  "last_portfolio_path": "/Users/philippe/Documents/portfolios/my_portfolio.csv"
}
```

---

## 5. Real-Time Market Feeds (Detailed)

### 5.1 Goals
- Provide users with the latest market data for their ETF holdings.
- Ensure free access and no dependency on paid APIs.
- Prioritize reliability and simplicity over ultra-low latency.

### 5.2 Data Sources
1. **Yahoo Finance via `yfinance`** (default)
   - Provides daily close, open, high, low, and volume.
   - Example: `yfinance.Ticker('EWLD.PA').history(period='1d')`
   - Limitations: Intraday data may be delayed.

2. **Euronext Public API (Optional fallback)**
   - Some ETFs listed on Euronext can be queried via their public data endpoints.
   - Use for cross-validation or where Yahoo data is incomplete.

3. **CSV Fallback**
   - User can upload a local CSV with columns: `Ticker,Date,Close`.

### 5.3 Update Frequency
- **Default:** Fetch at startup and on manual refresh (via UI button).
- **Optional Auto-Update:** Every 5 minutes during market hours (configurable in settings).

### 5.4 Error Handling
- If network request fails:
  - Display last cached price.
  - Log error in local `error.log` file.
  - Notify user in the UI with a tooltip or message bar.

### 5.5 Data Caching
- Cache latest price data locally to speed up loading and reduce API calls.
- Cache structure (JSON file):

```json
{
  "timestamp": "2025-11-08T10:15:00",
  "prices": {
    "EWLD.PA": 29.35,
    "PE500.PA": 43.12
  }
}
```

---

## 6. Architecture Overview

### 6.1 Modules Breakdown
| Module | Responsibility |
|---------|----------------|
| `main.py` | Entry point, initializes UI |
| `ui/` | PyQt6 UI components and layouts |
| `data/market_data.py` | Fetches and caches market data |
| `data/portfolio.py` | Manages portfolio calculations and persistence |
| `analytics/performance.py` | Computes metrics and risk analytics |
| `analytics/optimization.py` | Handles mean-variance optimization (Phase 2) |
| `config/settings.py` | Loads/saves user preferences |
| `visuals/charts.py` | Static Matplotlib/Plotly chart generation |

### 6.2 Data Flow
1. **User launches app →** loads preferences & last portfolio.
2. **Market Data Module →** fetches ETF prices via API or cache.
3. **Portfolio Module →** updates valuations and performance.
4. **UI →** displays charts, KPIs, and risk metrics.

---

## 7. Roadmap and Milestones

### Version 1.0 (MVP - Simulated Portfolio Tracker)
**Goal:** Build a stable, educational app with basic features.

**Deliverables:**
- PyQt6 user interface (menus, forms, and charts)
- Portfolio import/export via CSV
- Market data retrieval (Yahoo Finance + caching)
- Static performance and allocation charts
- Local settings and preferences persistence
- Packaged `.app` for macOS

**Estimated Duration:** 6–8 weeks

### Version 1.1 (Quality and UX Enhancements)
**Goal:** Improve user experience and reliability.

**Deliverables:**
- Auto-refresh option for market data
- Enhanced error handling and logging
- Additional chart options (e.g., volatility trend)
- Portfolio snapshots (save/load history)

**Estimated Duration:** 3–4 weeks

### Version 2.0 (Analytics Expansion)
**Goal:** Introduce advanced portfolio analytics.

**Deliverables:**
- Correlation matrix visualization
- Risk-adjusted return metrics (Sharpe, Sortino)
- Maximum drawdown visualization
- Improved reporting (PDF/CSV export)

**Estimated Duration:** 6–8 weeks

### Version 3.0 (Portfolio Optimization)
**Goal:** Introduce optimization and simulation tools.

**Deliverables:**
- Mean-variance optimization (Markowitz)
- Rebalancing simulator
- Strategy comparison tool (e.g., passive vs optimized portfolio)

**Estimated Duration:** 8–10 weeks

---

## 8. Future Enhancements
- Live interactive charts (Plotly or PyQtGraph).
- Multi-portfolio management.
- Backtesting module.
- Simple trading signals (momentum, mean reversion).

---

## 9. Deliverables (v1.0)
1. Fully functional PyQt6 interface.
2. Simulated PEA-eligible ETF portfolio.
3. Free real-time (or daily) market data integration.
4. Local persistence of user preferences and portfolio.
5. Static visualization of performance and allocation.
6. Packaged `.app` for macOS installation.