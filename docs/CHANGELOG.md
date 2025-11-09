# Changelog

All notable changes to PEA ETF Tracker will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.0] - 2025-11-09

### Added

**Core Features:**
- PyQt6 desktop application with native macOS UI
- Portfolio management with add/edit/delete ETF positions
- Real-time price fetching from Yahoo Finance API
- Offline price caching for portfolio tracking without internet
- CSV import/export for portfolio data
- JSON persistence for portfolio and settings

**Analytics Engine:**
- Portfolio value and P&L calculations
- Performance metrics: daily, weekly, monthly returns
- Risk analytics: volatility (standard deviation)
- Sharpe ratio (risk-adjusted returns)
- Maximum drawdown analysis
- Asset correlation matrix
- Position allocation percentages

**Visualization:**
- Interactive Plotly charts embedded in UI
- Portfolio value over time (line chart)
- Asset allocation (pie chart and bar chart)
- Risk vs Return scatter plot
- Individual ETF performance charts
- Chart export to PNG and HTML formats

**User Interface:**
- Main window with tabbed interface (Portfolio, Dashboard, Charts)
- Portfolio table with sortable columns and real-time updates
- Dashboard with KPI cards (Total Value, P&L, P&L %, Positions Count)
- Add/Edit position dialog with date picker
- Settings dialog with General and Charts tabs
- Context menu for portfolio positions (Edit/Delete)
- Status bar with portfolio summary
- Auto-refresh functionality with configurable interval

**Settings & Persistence:**
- User settings stored in `~/Library/Application Support/PEA_ETF_Tracker/config.json`
- Window geometry persistence (size, position)
- Chart preferences (color scheme, grid, legend)
- Currency selection (EUR, USD, GBP, CHF)
- Auto-refresh configuration
- Last portfolio path remembered

**Testing & Quality:**
- 174 comprehensive tests (unit + integration)
- ~78% code coverage
- Black code formatting (100%)
- Pylint scores 8.0-10.0/10
- MyPy type checking with 0 errors
- pytest-qt for GUI testing

### Known Limitations

**API & Performance:**
- Yahoo Finance rate limits: avoid refreshing >50 tickers/minute
- Network dependency for price fetching (cached fallback available)
- Chart export requires kaleido package for PNG export
- Auto-refresh during market hours not implemented (manual F5 only)

**Platform:**
- macOS only (tested on macOS Sonoma)
- Windows/Linux support not tested (PyQt6 is cross-platform compatible)

**Features:**
- No live price streaming (manual refresh required)
- No portfolio alerts or notifications
- No multi-portfolio comparison view
- No backtesting capabilities
- No transaction history tracking
- No tax reporting features

### Technical Details

**Dependencies:**
- Python 3.11+
- PyQt6 6.6.1 (UI framework)
- yfinance 0.2.32 (market data)
- plotly 5.18.0 (charts)
- pandas 2.1.4 (data processing)
- numpy 1.26.2 (numerical calculations)
- pytest 7.4.3 + pytest-qt 4.2.0 (testing)

**File Locations (macOS):**
- Config: `~/Library/Application Support/PEA_ETF_Tracker/config.json`
- Cache: `~/Library/Application Support/PEA_ETF_Tracker/cache/`
- Logs: `~/Library/Logs/PEA_ETF_Tracker/app.log`

### Future Enhancements (v1.1+)

**Planned Features:**
- Auto-refresh during market hours (trading session detection)
- Portfolio snapshots (historical state tracking)
- Enhanced error messages with retry logic
- Improved chart export options (SVG, PDF)
- Multi-language support (French translation)
- Correlation matrix heatmap visualization
- Portfolio rebalancing calculator
- Enhanced reporting (PDF export)

**Long-term (v2.0+):**
- Mean-variance optimization (Markowitz model)
- Efficient frontier visualization
- Monte Carlo simulations
- Backtesting engine
- Strategy comparison tools
- Tax lot tracking
- Dividend tracking and reinvestment
- Multi-currency portfolio support

### Migration Notes

This is the initial v1.0 release - no migration needed.

### Contributors

- Philippe Avarre (Project Lead & Developer)

### License

This project is for educational and personal portfolio management purposes.

---

## Release Schedule

- **v1.0.0** (2025-11-09): Initial MVP release
- **v1.1.0** (Planned Q1 2026): Auto-refresh, snapshots, enhanced UX
- **v2.0.0** (Planned Q2 2026): Portfolio optimization, backtesting

---

**Note:** This is a personal finance tool. Always verify calculations independently and consult with financial advisors for investment decisions.
