# PEA ETF Tracker - User Guide

**Version:** 1.0.0
**Last Updated:** 2025-11-09

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Your First Portfolio](#your-first-portfolio)
3. [Managing Positions](#managing-positions)
4. [Refreshing Market Data](#refreshing-market-data)
5. [Understanding Analytics](#understanding-analytics)
6. [Viewing Charts](#viewing-charts)
7. [Import & Export](#import--export)
8. [Settings](#settings)
9. [Keyboard Shortcuts](#keyboard-shortcuts)
10. [Troubleshooting](#troubleshooting)
11. [FAQ](#faq)

---

## Getting Started

### Installation

**Prerequisites:**
- macOS 10.15 (Catalina) or later
- Python 3.11 or later

**Installation Steps:**

1. **Navigate to project directory:**
   ```bash
   cd "/Users/philippe/Documents/ETF Manager"
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Launch the application:**
   ```bash
   python main.py
   ```

**First Launch:**
- Application creates config directory: `~/Library/Application Support/PEA_ETF_Tracker/`
- Default settings are created automatically
- Empty portfolio is initialized

---

## Your First Portfolio

### Quick Start Tutorial

**Step 1: Import Demo Portfolio**

1. Launch the application
2. Click **File → Import from CSV**
3. Navigate to `sample_data/demo_portfolio.csv`
4. Click **Open**
5. Portfolio loads with 5 PEA-eligible ETFs

**Step 2: Refresh Prices**

1. Press **F5** or click **Refresh** button
2. Wait for prices to download from Yahoo Finance (5-10 seconds)
3. Current prices populate in the table
4. P&L columns calculate automatically

**Step 3: View Dashboard**

1. Click **Dashboard** tab
2. See KPI cards:
   - Total Value
   - Total Invested
   - P&L (€)
   - P&L (%)
   - Number of Positions

**Step 4: Explore Charts**

1. Click **Charts** tab
2. Select chart type from dropdown:
   - Portfolio Value Over Time
   - Allocation (Pie Chart)
   - Allocation (Bar Chart)
   - Risk vs Return
   - Performance

---

## Managing Positions

### Adding a New Position

1. Click **Edit → Add Position** (or Ctrl+A)
2. Fill in the dialog:
   - **Ticker:** ETF ticker symbol (e.g., `EWLD.PA`)
   - **Name:** ETF name (e.g., `Amundi MSCI World`)
   - **Quantity:** Number of shares (e.g., `100`)
   - **Buy Price:** Purchase price in EUR (e.g., `28.50`)
   - **Buy Date:** Purchase date (use date picker)
3. Click **OK**
4. Position appears in portfolio table

**PEA-Eligible ETF Tickers (Examples):**
- `EWLD.PA` - Amundi MSCI World
- `PE500.PA` - Lyxor S&P 500
- `PAEEM.PA` - Lyxor MSCI Emerging Markets
- `PCEU.PA` - Lyxor STOXX Europe 600
- `PSP5.PA` - Amundi MSCI Europe

### Editing a Position

1. **Right-click** on position row in table
2. Select **Edit Position**
3. Modify fields (ticker is read-only)
4. Click **OK**
5. Table updates automatically

### Deleting a Position

1. **Right-click** on position row
2. Select **Delete Position**
3. Confirm deletion
4. Position removed from portfolio

---

## Refreshing Market Data

### Manual Refresh

**Method 1: Keyboard**
- Press **F5**

**Method 2: Menu**
- Click **Edit → Refresh Prices**

**Method 3: Toolbar**
- Click **Refresh** button

**What Happens:**
- Application fetches latest prices from Yahoo Finance
- Prices cached to `~/Library/Application Support/PEA_ETF_Tracker/cache/`
- P&L recalculated for all positions
- Dashboard KPIs updated
- Status bar shows portfolio value

**Refresh Time:** ~2-5 seconds for 10 ETFs (depends on network speed)

### Auto-Refresh (Optional)

1. Open **Settings → General** tab
2. Check **Enable Auto-Refresh**
3. Set interval (default: 5 minutes)
4. Click **Apply**

**Note:** Auto-refresh works even when app is in background

### Offline Mode

If no internet connection:
- Application uses **cached prices** from last successful refresh
- Status bar shows "(Cached)" indicator
- Charts display based on cached data

---

## Understanding Analytics

### Portfolio Metrics

**Total Value:**
- Sum of (Current Price × Quantity) for all positions
- Formula: `Σ (price_i × quantity_i)`

**Total Invested:**
- Sum of (Buy Price × Quantity) for all positions
- Formula: `Σ (buy_price_i × quantity_i)`

**P&L (Profit & Loss):**
- Difference between Total Value and Total Invested
- Formula: `Total Value - Total Invested`

**P&L %:**
- Percentage gain or loss
- Formula: `(P&L / Total Invested) × 100`

### Risk Analytics

**Volatility (σ):**
- Standard deviation of returns
- Measures price fluctuation
- Formula: `σ = √(Σ(r_i - μ)² / (n-1))`
  - Where `r_i` = returns, `μ` = mean return

**Sharpe Ratio:**
- Risk-adjusted return metric
- Higher is better (>1 is good, >2 is excellent)
- Formula: `S = (R_p - R_f) / σ_p`
  - Where `R_p` = portfolio return, `R_f` = risk-free rate, `σ_p` = volatility

**Maximum Drawdown:**
- Largest peak-to-trough decline
- Measures downside risk
- Formula: `Max DD = (Trough Value - Peak Value) / Peak Value`

**Correlation:**
- Measures how ETFs move together
- Range: -1 (opposite) to +1 (together)
- Used for diversification analysis

---

## Viewing Charts

### Available Chart Types

**1. Portfolio Value Over Time**
- Line chart showing total portfolio value
- X-axis: Time (dates)
- Y-axis: Portfolio value (EUR)
- Use: Track portfolio growth

**2. Allocation (Pie Chart)**
- Circular chart showing position breakdown
- Each slice = % of total portfolio value
- Use: Visualize diversification

**3. Allocation (Bar Chart)**
- Bar chart showing position values
- X-axis: ETF tickers
- Y-axis: Position value (EUR)
- Use: Compare position sizes

**4. Risk vs Return**
- Scatter plot of ETFs
- X-axis: Volatility (risk)
- Y-axis: Returns
- Use: Identify high return / low risk ETFs

**5. Performance Chart**
- Line chart of individual ETF price history
- X-axis: Time
- Y-axis: Price (EUR)
- Use: Analyze individual ETF trends

### Exporting Charts

1. Display desired chart
2. Click **Export PNG** or **Export HTML**
3. Choose save location
4. Chart saved to file

**PNG Export:**
- Static image (requires kaleido)
- Suitable for presentations

**HTML Export:**
- Interactive chart
- Can zoom/pan in browser

---

## Import & Export

### Import Portfolio from CSV

1. Click **File → Import from CSV**
2. Select CSV file
3. Verify data preview
4. Click **Confirm**

**CSV Format:**
```csv
Ticker,Name,Quantity,BuyPrice,BuyDate
EWLD.PA,Amundi MSCI World,100,28.50,2024-01-15
PE500.PA,Lyxor S&P 500,50,42.30,2024-02-10
```

**Required Columns:**
- `Ticker` - ETF ticker symbol
- `Name` - ETF name
- `Quantity` - Number of shares (positive number)
- `BuyPrice` - Purchase price (positive number)
- `BuyDate` - Date in YYYY-MM-DD format

### Export Portfolio to CSV

1. Click **File → Export to CSV**
2. Choose save location
3. Enter filename (e.g., `my_portfolio.csv`)
4. Click **Save**

**Use Cases:**
- Backup portfolio data
- Share with financial advisor
- Import into spreadsheet software

### Save Portfolio (JSON)

1. Click **File → Save** (Ctrl+S)
2. Portfolio saved to current file path
3. Or **File → Save As** to save new file

**JSON Format:**
- Human-readable
- Includes all position data
- Stored in `~/Documents/` by default

---

## Settings

### General Tab

**Currency:**
- EUR (default)
- USD
- GBP
- CHF

**Data Source:**
- Yahoo Finance (only option in v1.0)

**Auto-Refresh:**
- Enable/Disable auto-refresh
- Interval: 1-60 minutes
- Default: 5 minutes

**Last Portfolio:**
- Automatically loads last opened portfolio on startup

### Charts Tab

**Color Scheme:**
- Plotly (default, colorful)
- Pastel (soft colors)
- Bold (high contrast)

**Display Options:**
- Show Grid (on/off)
- Show Legend (on/off)

**Applying Settings:**
- Click **OK** to apply and close
- Click **Apply** to apply without closing
- Click **Cancel** to discard changes
- Click **Restore Defaults** to reset

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Cmd+N` / `Ctrl+N` | New Portfolio |
| `Cmd+O` / `Ctrl+O` | Open Portfolio |
| `Cmd+S` / `Ctrl+S` | Save Portfolio |
| `Cmd+Shift+S` | Save Portfolio As |
| `Cmd+I` / `Ctrl+I` | Import from CSV |
| `Cmd+E` / `Ctrl+E` | Export to CSV |
| `F5` | Refresh Market Data |
| `Cmd+A` / `Ctrl+A` | Add Position |
| `Cmd+,` / `Ctrl+,` | Settings |
| `Cmd+Q` / `Ctrl+Q` | Quit Application |

**Table Navigation:**
- Arrow keys: Navigate rows
- Click column header: Sort by column
- Right-click row: Context menu

---

## Troubleshooting

### Market Data Not Updating

**Problem:** Prices don't refresh when pressing F5

**Solutions:**
1. Check internet connection
2. Verify Yahoo Finance is accessible: https://finance.yahoo.com
3. Check ticker symbols are correct (must include `.PA` for Euronext Paris)
4. View logs: `~/Library/Logs/PEA_ETF_Tracker/app.log`
5. Clear cache: Delete `~/Library/Application Support/PEA_ETF_Tracker/cache/`

### Portfolio Won't Load

**Problem:** Error when opening portfolio file

**Solutions:**
1. Verify file is valid JSON (open in text editor)
2. Check file permissions (must be readable)
3. Try importing from CSV instead
4. Restore from backup if available
5. Create new portfolio and re-enter positions

### Application Won't Start

**Problem:** App crashes on launch

**Solutions:**
1. Verify Python version: `python3 --version` (must be 3.11+)
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check for error messages in terminal
4. Delete config file: `~/Library/Application Support/PEA_ETF_Tracker/config.json`
5. Check logs: `~/Library/Logs/PEA_ETF_Tracker/app.log`

### Charts Not Displaying

**Problem:** Charts tab is blank or shows error

**Solutions:**
1. Refresh prices first (charts need data)
2. Verify plotly is installed: `pip show plotly`
3. Check PyQt6-WebEngine installed: `pip show PyQt6-WebEngine`
4. Restart application
5. Try exporting to HTML instead

### SSL Certificate Errors

**Problem:** yfinance SSL errors when fetching prices

**Solutions (macOS):**
1. Upgrade certifi: `pip install --upgrade certifi`
2. Run certificate installer:
   ```bash
   /Applications/Python\ 3.11/Install\ Certificates.command
   ```
3. Or install certificates manually:
   ```bash
   pip install --upgrade certifi
   ```

---

## FAQ

**Q: What does PEA mean?**
A: Plan d'Épargne en Actions - French tax-advantaged savings account for European stocks/ETFs.

**Q: Does this track real trades?**
A: No, this is a portfolio simulation/tracking tool. It doesn't execute real trades.

**Q: Are prices real-time?**
A: Prices are delayed ~15 minutes (Yahoo Finance free tier). Press F5 to get latest.

**Q: Can I track US ETFs?**
A: Yes, but focus is on PEA-eligible (European) ETFs. Use US tickers like `SPY` without `.PA`.

**Q: How often should I refresh prices?**
A: Daily is sufficient for long-term investors. Intraday tracking requires auto-refresh.

**Q: Is my data secure?**
A: All data stored locally on your Mac. No cloud sync. Backup your portfolio files regularly.

**Q: Can I track multiple portfolios?**
A: Yes, save multiple portfolio JSON files and open as needed (File → Open).

**Q: What's the maximum number of positions?**
A: No hard limit, but performance may degrade beyond 100 positions.

**Q: Can I export to Excel?**
A: Export to CSV, then open in Excel/Numbers.

**Q: Does it work offline?**
A: Partially - uses cached prices. Refresh requires internet.

**Q: Where are backups stored?**
A: No automatic backups. Save portfolio files manually (File → Save As).

---

## Getting Help

**Documentation:**
- README.md - Installation and quick start
- CHANGELOG.md - Version history and features
- PROJECT_PLAN.md - Development roadmap

**Logs:**
- Location: `~/Library/Logs/PEA_ETF_Tracker/app.log`
- Contains error messages and debugging info

**Sample Data:**
- `sample_data/demo_portfolio.csv` - Example portfolio
- `sample_data/sample_etfs.json` - PEA-eligible ETF list

---

**Version:** 1.0.0
**Support:** Check logs and documentation
**License:** Educational/Personal Use

**Happy tracking! 📈**
