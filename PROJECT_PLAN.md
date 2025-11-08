# PEA ETF Tracker - Version 1.0 MVP Implementation Plan

## Overview
Build a complete PEA-eligible ETF portfolio tracker with PyQt6 UI, real-time market data from Yahoo Finance, portfolio analytics, and data visualization. Following TDD principles and strict Python best practices from AI_CODING_RULES.md.

**Timeline:** 8 weeks
**Status:** Phase 1 - Complete ✅ | Phase 2 - Ready to Start
**Last Updated:** 2025-11-08

---

## **Phase 1: Project Foundation & Setup** (Week 1)

**Status:** ✅ COMPLETE
**Goal:** Establish project structure, configure development tooling, set up dependencies and environment
**Completed:** 2025-11-08

### Tasks

- [x] **Project Structure**
  - [x] Create module directories: `ui/`, `data/`, `analytics/`, `config/`, `visuals/`, `tests/`
  - [x] Create `__init__.py` files for all modules
  - [x] Set up main entry point `main.py`

- [x] **Development Configuration**
  - [x] Create `requirements.txt` with: PyQt6, yfinance, plotly, pandas, numpy, pytest, black, pylint, mypy
  - [x] Create `.gitignore` (Python, PyQt, IDE, macOS specific)
  - [x] Initialize git repository
  - [x] Create `README.md` with installation and usage instructions
  - [x] Create `pyproject.toml` for black/pylint/mypy configuration

- [x] **Tooling Setup**
  - [x] Install all dependencies in virtual environment (48 packages)
  - [x] Configure black formatter
  - [x] Configure pylint/flake8 linting
  - [x] Configure mypy type checking
  - [x] Set up pytest structure

- [x] **Sample Data**
  - [x] Create sample ETF data for PEA-eligible ETFs (EWLD.PA, PE500.PA, etc.)
  - [x] Create demo portfolio CSV template
  - [x] Create sample config.json structure

### Deliverables
- ✅ Complete project structure
- ✅ All tooling configured and passing
- ✅ Git repository initialized
- ✅ Dependencies installed

### Quality Gates - PASSED ✅
```bash
black .                    # ✅ 7 files formatted
pylint main.py ui/ data/ analytics/ config/ visuals/ tests/  # ✅ Score: 8.89/10
mypy main.py ui/ data/ analytics/ config/ visuals/  # ✅ No issues found
pytest tests/ -v          # ✅ Infrastructure ready (0 tests, as expected)
```

### Phase 1 Results
- **17 files created and committed**
- **48 Python packages installed**
- **Pylint score:** 8.89/10 (exceeds 8.0 requirement)
- **Mypy errors:** 0
- **Git commit:** 1d9eae9 (feat: initialize project structure)

---

## **Phase 2: Core Data Models & Configuration** (Week 2)

**Status:** ⬜ Not Started
**Goal:** Implement configuration management, build core data structures, create portfolio persistence layer

### Tasks

- [ ] **Configuration Module (`config/settings.py`)**
  - [ ] Implement `Settings` dataclass with type hints
  - [ ] Implement `load_settings()` from `~/Library/Application Support/PEA_ETF_Tracker/config.json`
  - [ ] Implement `save_settings()` with error handling
  - [ ] Provide default configuration fallback
  - [ ] Create `tests/test_settings.py` - test load/save/defaults/corruption handling

- [ ] **Portfolio Data Models (`data/portfolio.py`)**
  - [ ] Create `ETFPosition` dataclass (ticker, name, quantity, buy_price, buy_date)
  - [ ] Create `Portfolio` class with positions list
  - [ ] Implement `add_position()`, `remove_position()`, `update_position()`
  - [ ] Implement `save_to_json()`, `load_from_json()`
  - [ ] Implement CSV import/export methods
  - [ ] Create `tests/test_portfolio.py` - test CRUD operations, persistence, CSV import/export

- [ ] **Market Data Module (`data/market_data.py`)**
  - [ ] Implement `fetch_price(ticker: str)` using yfinance
  - [ ] Implement price caching to JSON file
  - [ ] Implement `fetch_historical_data(ticker, period)`
  - [ ] Error handling and logging for network failures
  - [ ] Fallback to cached data when offline
  - [ ] Create `tests/test_market_data.py` - test fetch, cache, error handling

### Deliverables
- ✅ Configuration persistence working
- ✅ Portfolio CRUD operations functional
- ✅ Market data fetching with caching
- ✅ All tests passing (black, pylint, mypy, pytest)

### Quality Gates
```bash
black config/ data/ tests/
pylint config/settings.py data/portfolio.py data/market_data.py  # Score ≥ 8.0
mypy config/settings.py data/portfolio.py data/market_data.py    # No errors
pytest tests/test_settings.py tests/test_portfolio.py tests/test_market_data.py -v
```

---

## **Phase 3: Portfolio Analytics Engine** (Week 3)

**Status:** ⬜ Not Started
**Goal:** Implement performance calculations, build risk analytics, create metrics calculation engine

### Tasks

- [ ] **Performance Analytics (`analytics/performance.py`)**
  - [ ] Implement `calculate_portfolio_value(portfolio, prices)`
  - [ ] Implement `calculate_returns(portfolio, historical_prices)` - daily, weekly, monthly
  - [ ] Implement `calculate_pnl(portfolio, current_prices)`
  - [ ] Implement `calculate_allocation_by_value(portfolio, prices)`
  - [ ] Create `tests/test_performance.py` - test calculations with known inputs

- [ ] **Risk Analytics (`analytics/performance.py`)**
  - [ ] Implement `calculate_volatility(returns)`
  - [ ] Implement `calculate_sharpe_ratio(returns, risk_free_rate)`
  - [ ] Implement `calculate_max_drawdown(portfolio_values)`
  - [ ] Implement `calculate_correlation_matrix(historical_data)`
  - [ ] Create `tests/test_risk_analytics.py` - test with realistic data

- [ ] **Optimization Stub (`analytics/optimization.py`)**
  - [ ] Create placeholder module for Phase 2
  - [ ] Add basic structure and docstrings
  - [ ] No implementation needed for MVP

### Deliverables
- ✅ Complete analytics engine
- ✅ Accurate financial calculations
- ✅ All tests passing with good coverage

### Quality Gates
```bash
black analytics/ tests/
pylint analytics/performance.py analytics/optimization.py  # Score ≥ 8.0
mypy analytics/performance.py analytics/optimization.py    # No errors
pytest tests/test_performance.py tests/test_risk_analytics.py -v --cov=analytics
```

---

## **Phase 4: Visualization Components** (Week 4)

**Status:** ⬜ Not Started
**Goal:** Build static chart generation, create portfolio visualization functions, implement Plotly charts

### Tasks

- [ ] **Chart Generation (`visuals/charts.py`)**
  - [ ] Implement `create_portfolio_value_chart(dates, values)` - line chart
  - [ ] Implement `create_allocation_pie_chart(positions, values)` - pie chart
  - [ ] Implement `create_allocation_bar_chart(sectors, percentages)` - bar chart
  - [ ] Implement `create_risk_return_scatter(etfs, returns, volatilities)` - scatter plot
  - [ ] Implement `create_performance_chart(etf_name, historical_data)` - candlestick/line
  - [ ] All functions return Plotly figure objects
  - [ ] Create `tests/test_charts.py` - test chart creation, verify structure

- [ ] **Chart Utilities**
  - [ ] Implement color schemes and themes
  - [ ] Implement chart export to PNG/HTML
  - [ ] Error handling for missing data

### Deliverables
- ✅ Complete chart generation library
- ✅ Plotly charts working and styled
- ✅ Export functionality implemented

### Quality Gates
```bash
black visuals/ tests/
pylint visuals/charts.py  # Score ≥ 8.0
mypy visuals/charts.py    # No errors
pytest tests/test_charts.py -v --cov=visuals
```

---

## **Phase 5: PyQt6 User Interface - Core** (Week 5)

**Status:** ⬜ Not Started
**Goal:** Build main application window, create menu and toolbar, implement basic navigation

### Tasks

- [ ] **Main Window (`ui/main_window.py`)**
  - [ ] Create `MainWindow` class inheriting `QMainWindow`
  - [ ] Implement menu bar (File, Edit, View, Help)
  - [ ] Implement toolbar with common actions
  - [ ] Create central widget with tab layout
  - [ ] Status bar with connection status
  - [ ] Create `tests/test_integration.py` - GUI integration tests

- [ ] **Application Entry Point (`main.py`)**
  - [ ] Initialize QApplication
  - [ ] Load settings and last portfolio
  - [ ] Create and show MainWindow
  - [ ] Set up event loop
  - [ ] Error handling and logging

- [ ] **Portfolio Table Widget (`ui/portfolio_table.py`)**
  - [ ] Create `PortfolioTableWidget` with columns: Ticker, Name, Quantity, Buy Price, Current Price, P&L, P&L %
  - [ ] Implement add/edit/remove position dialogs
  - [ ] Implement table sorting and filtering
  - [ ] Real-time price updates in table
  - [ ] Add integration tests for table interactions

### Deliverables
- ✅ Functional main window
- ✅ Portfolio table with CRUD operations
- ✅ Menu and toolbar working

### Quality Gates
```bash
black ui/ main.py tests/
pylint ui/main_window.py ui/portfolio_table.py main.py  # Score ≥ 8.0
mypy ui/main_window.py ui/portfolio_table.py main.py    # No errors
pytest tests/test_integration.py -v
```

---

## **Phase 6: PyQt6 User Interface - Features** (Week 6)

**Status:** ⬜ Not Started
**Goal:** Implement chart display widgets, create settings dialog, build import/export UI

### Tasks

- [ ] **Chart Display Widget (`ui/chart_widget.py`)**
  - [ ] Create `ChartWidget` for embedding Plotly charts
  - [ ] Implement chart type selector (dropdown)
  - [ ] Implement refresh button
  - [ ] Handle chart updates and interactions
  - [ ] Add integration tests for chart display

- [ ] **Settings Dialog (`ui/settings_dialog.py`)**
  - [ ] Create dialog for user preferences
  - [ ] Currency selection
  - [ ] Data source selection
  - [ ] Auto-refresh settings
  - [ ] Chart preferences
  - [ ] Save/Cancel buttons
  - [ ] Add integration tests for settings persistence

- [ ] **Import/Export Dialogs (`ui/io_dialogs.py`)**
  - [ ] Create CSV import dialog with file picker
  - [ ] Create CSV export dialog
  - [ ] Preview imported data before confirming
  - [ ] Error handling and validation
  - [ ] Add integration tests for import/export flows

- [ ] **Dashboard Widget (`ui/dashboard.py`)**
  - [ ] Create dashboard with KPI cards (total value, total P&L, daily change)
  - [ ] Display key metrics (Sharpe ratio, volatility, max drawdown)
  - [ ] Summary statistics table
  - [ ] Add integration tests for dashboard updates

### Deliverables
- ✅ Complete UI with all features
- ✅ Settings persistence working
- ✅ Import/export functional
- ✅ Dashboard displaying metrics

### Quality Gates
```bash
black ui/ tests/
pylint ui/chart_widget.py ui/settings_dialog.py ui/io_dialogs.py ui/dashboard.py  # Score ≥ 8.0
mypy ui/chart_widget.py ui/settings_dialog.py ui/io_dialogs.py ui/dashboard.py    # No errors
pytest tests/test_integration.py -v --cov=ui
```

---

## **Phase 7: Integration & Data Flow** (Week 7)

**Status:** ⬜ Not Started
**Goal:** Connect all components, implement data refresh logic, build complete user workflows

### Tasks

- [ ] **Application Integration**
  - [ ] Connect market data fetching to UI refresh
  - [ ] Link portfolio changes to analytics updates
  - [ ] Connect analytics to chart generation
  - [ ] Implement auto-save on portfolio changes
  - [ ] Handle application startup sequence

- [ ] **Workflows Implementation**
  - [ ] Add new ETF position workflow
  - [ ] Edit existing position workflow
  - [ ] Delete position workflow
  - [ ] Import portfolio from CSV workflow
  - [ ] Export portfolio to CSV workflow
  - [ ] Manual price refresh workflow
  - [ ] Change settings workflow

- [ ] **Error Handling & Logging**
  - [ ] Implement application-wide error handler
  - [ ] Set up logging to file (`~/Library/Logs/PEA_ETF_Tracker/app.log`)
  - [ ] User-friendly error messages in UI
  - [ ] Network error handling and retry logic

- [ ] **Integration Tests (`tests/test_integration.py`)**
  - [ ] Test complete workflows end-to-end
  - [ ] Test data persistence across app restarts
  - [ ] Test offline mode with cached data
  - [ ] Test error recovery scenarios

### Deliverables
- ✅ Fully integrated application
- ✅ All workflows functional
- ✅ Comprehensive error handling
- ✅ Integration tests passing

### Quality Gates
```bash
black .
pylint **/*.py  # Score ≥ 8.0 for all modules
mypy .          # No errors
pytest tests/ -v --cov=. --cov-report=html
```

---

## **Phase 8: Polish, Testing & Documentation** (Week 8)

**Status:** ⬜ Not Started
**Goal:** Comprehensive testing, code quality gates, complete documentation, macOS packaging

### Tasks

- [ ] **Testing & Quality Assurance**
  - [ ] Achieve >80% test coverage
  - [ ] Run full test suite: `pytest tests/`
  - [ ] Format all code: `black .`
  - [ ] Lint all code: `pylint` or `flake8` (score ≥ 8.0)
  - [ ] Type check: `mypy` strict mode
  - [ ] Fix all issues

- [ ] **Documentation**
  - [ ] Complete README.md with installation, usage, screenshots
  - [ ] Add docstrings to all public functions (Google style)
  - [ ] Create user guide for common tasks
  - [ ] Document keyboard shortcuts and UI interactions
  - [ ] Add mathematical documentation for analytics

- [ ] **Sample Data & Demo**
  - [ ] Create comprehensive sample portfolio
  - [ ] Include 5-10 PEA-eligible ETFs with realistic data
  - [ ] Pre-populate demo config.json
  - [ ] Create tutorial walkthrough

- [ ] **macOS Packaging (`packaging/`)**
  - [ ] Create PyInstaller spec file
  - [ ] Configure app bundle settings (icon, info.plist)
  - [ ] Test packaged .app on clean macOS system
  - [ ] Create installation instructions
  - [ ] Verify app works without Python installed

- [ ] **Performance Optimization**
  - [ ] Profile application startup time
  - [ ] Optimize chart rendering
  - [ ] Cache frequently accessed data
  - [ ] Ensure UI responsiveness

### Deliverables
- ✅ Complete test suite passing
- ✅ All quality gates passing (black, pylint, mypy)
- ✅ Comprehensive documentation
- ✅ Packaged .app for macOS
- ✅ v1.0 ready for release

### Quality Gates
```bash
# Final quality check
black .
pylint **/*.py --fail-under=8.0
mypy . --strict
pytest tests/ -v --cov=. --cov-report=html --cov-fail-under=80

# Packaging
pyinstaller pea_etf_tracker.spec
open dist/PEA_ETF_Tracker.app
```

---

## Code Quality Standards (Every Phase)

Following [AI_CODING_RULES.md](AI_CODING_RULES.md):

### Before Coding
- ✅ Ask clarifying questions
- ✅ Draft approach for complex features
- ✅ List pros/cons for design decisions

### While Coding
- ✅ Follow TDD: stub → test → implement
- ✅ Type hints on all functions
- ✅ Use dataclasses for config objects
- ✅ PEP 8 naming conventions
- ✅ Context managers for file operations
- ✅ NumPy vectorization for numerical ops
- ✅ pathlib.Path for file paths
- ✅ Descriptive variable and function names

### Testing (pytest)
- ✅ Tests in `tests/` directory
- ✅ Separate unit tests from integration tests
- ✅ Parametrize test inputs
- ✅ Descriptive test names
- ✅ Use fixtures for common setup

### Quality Gates (Every Commit)
```bash
black .                    # Format
pylint <module>.py        # Lint (≥8.0)
mypy <module>.py          # Type check
pytest tests/             # Tests pass
```

### Git Commits
- ✅ Conventional Commits format
- ✅ Atomic commits
- ✅ Descriptive messages (why, not what)

---

## Technology Stack Summary

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Language | Python 3.11+ | Core application |
| UI Framework | PyQt6 | Native macOS interface |
| Data Source | Yahoo Finance (yfinance) | Market data |
| Visualization | Plotly | Interactive charts |
| Data Processing | Pandas, NumPy | Analytics calculations |
| Persistence | JSON | Portfolio & settings storage |
| Testing | pytest | Test framework |
| Formatting | black | Code formatting |
| Linting | pylint/flake8 | Code quality |
| Type Checking | mypy | Static type analysis |
| Packaging | PyInstaller | macOS .app bundle |

---

## Project Structure

```
ETF Manager/
├── main.py                           # Application entry point
├── requirements.txt                  # Python dependencies
├── pyproject.toml                    # Tool configuration (black, pylint, mypy)
├── .gitignore                        # Git ignore rules
├── README.md                         # User documentation
├── PROJECT_PLAN.md                   # This file
├── AI_CODING_RULES.md               # Coding standards
├── Product Requirements Document.md  # PRD
│
├── ui/                              # PyQt6 UI components
│   ├── __init__.py
│   ├── main_window.py               # Main application window
│   ├── portfolio_table.py           # Portfolio table widget
│   ├── chart_widget.py              # Chart display widget
│   ├── settings_dialog.py           # Settings dialog
│   ├── io_dialogs.py                # Import/export dialogs
│   └── dashboard.py                 # Dashboard widget
│
├── data/                            # Data management
│   ├── __init__.py
│   ├── market_data.py               # Market data fetching and caching
│   └── portfolio.py                 # Portfolio models and persistence
│
├── analytics/                       # Portfolio analytics
│   ├── __init__.py
│   ├── performance.py               # Performance and risk metrics
│   └── optimization.py              # Portfolio optimization (stub for v1.0)
│
├── config/                          # Configuration management
│   ├── __init__.py
│   └── settings.py                  # Settings persistence
│
├── visuals/                         # Chart generation
│   ├── __init__.py
│   └── charts.py                    # Plotly chart functions
│
├── tests/                           # Test suite
│   ├── __init__.py
│   ├── test_settings.py             # Settings tests
│   ├── test_portfolio.py            # Portfolio tests
│   ├── test_market_data.py          # Market data tests
│   ├── test_performance.py          # Performance analytics tests
│   ├── test_risk_analytics.py       # Risk analytics tests
│   ├── test_charts.py               # Chart generation tests
│   └── test_integration.py          # Integration tests
│
├── sample_data/                     # Sample data for testing
│   ├── demo_portfolio.csv           # Sample portfolio CSV
│   ├── demo_config.json             # Sample configuration
│   └── sample_etfs.json             # Sample ETF data
│
├── packaging/                       # Packaging configuration
│   ├── pea_etf_tracker.spec         # PyInstaller spec file
│   ├── icon.icns                    # macOS app icon
│   └── Info.plist                   # macOS app metadata
│
└── docs/                            # Documentation
    └── user_guide.md                # User guide
```

---

## Success Criteria for v1.0 MVP

- ✅ PyQt6 UI with all planned widgets
- ✅ Create/manage simulated ETF portfolio
- ✅ Add/edit/remove positions via UI
- ✅ Import/export portfolio from CSV
- ✅ Fetch real-time prices from Yahoo Finance
- ✅ Price caching for offline use
- ✅ Calculate performance metrics (returns, P&L)
- ✅ Calculate risk metrics (volatility, Sharpe, max drawdown)
- ✅ Display 4 chart types (portfolio value, allocation pie/bar, risk/return scatter)
- ✅ User preferences persistence
- ✅ Complete test coverage (>80%)
- ✅ All quality gates passing
- ✅ Packaged .app for macOS
- ✅ Complete documentation

---

## Progress Tracking

### Overall Progress: 1/8 Phases Complete (12.5%)

| Phase | Status | Completion |
|-------|--------|------------|
| Phase 1: Foundation | ✅ Complete | 100% |
| Phase 2: Core Data Models | 🔄 Ready to Start | 0% |
| Phase 3: Analytics Engine | ⬜ Not Started | 0% |
| Phase 4: Visualization | ⬜ Not Started | 0% |
| Phase 5: UI Core | ⬜ Not Started | 0% |
| Phase 6: UI Features | ⬜ Not Started | 0% |
| Phase 7: Integration | ⬜ Not Started | 0% |
| Phase 8: Polish & Packaging | ⬜ Not Started | 0% |

---

## Notes & Decisions

### Design Decisions
- **Data Persistence:** JSON chosen for simplicity and human-readability
- **Visualization:** Plotly chosen for modern, interactive charts and future extensibility
- **TDD Approach:** Following strict TDD throughout per AI_CODING_RULES.md

### Risks & Mitigation
- **Risk:** Yahoo Finance API reliability
  - **Mitigation:** Implement robust caching and CSV fallback option
- **Risk:** PyQt6 learning curve
  - **Mitigation:** Start with simple widgets, iterate based on testing
- **Risk:** Financial calculations accuracy
  - **Mitigation:** Comprehensive unit tests with known inputs/outputs

### Future Enhancements (Post v1.0)
- Live auto-refresh during market hours (v1.1)
- Enhanced error handling and logging (v1.1)
- Correlation matrix visualization (v2.0)
- Mean-variance optimization (v3.0)
- Backtesting module (v3.0+)

---

**Last Updated:** 2025-11-08
**Current Phase:** Phase 2 - Core Data Models & Configuration
**Next Review:** End of Phase 2

---

## Phase 2 Implementation Analysis & Patterns (Added 2025-11-08)

### Code Pattern Analysis from Phase 1 Foundation

#### From main.py - Key Patterns to Reuse:
1. **Module Docstring:** Google-style docstring at top with module purpose
2. **Pathlib Usage:** Always use `Path.home() / "Library/..."` for macOS paths
   ```python
   CONFIG_DIR = Path.home() / "Library/Application Support/PEA_ETF_Tracker"
   ```
3. **Logging Setup:** Initialize at module level, never use print()
   ```python
   logger = logging.getLogger(__name__)
   ```
4. **Type Hints:** All functions must have complete type hints
   ```python
   def load_settings(config_path: Path = CONFIG_FILE) -> Settings:
   ```
5. **Error Handling:** Use specific exception types, never bare except
   ```python
   except json.JSONDecodeError as e:
       logger.error(f"Invalid JSON: {e}")
   except FileNotFoundError as e:
       logger.warning(f"File not found: {e}")
   ```
6. **Context Managers:** Always use `with` for file I/O
   ```python
   with open(config_path, 'r') as f:
       config_dict = json.load(f)
   ```

#### From __init__.py Files - Pattern:
All __init__.py files follow consistent structure:
```python
"""
[Module Name] management module for PEA ETF Tracker.

This module handles:
- [Purpose 1]
- [Purpose 2]
"""

__version__ = "1.0.0"
```

### Sample Data Structure Analysis

#### demo_config.json Structure (Settings Dataclass):
```python
@dataclass
class ChartPreferences:
    default_chart: str = "portfolio_value"
    color_scheme: str = "plotly"
    show_grid: bool = True
    show_legend: bool = True

@dataclass
class WindowGeometry:
    width: int = 1200
    height: int = 800
    x: int = 100
    y: int = 100

@dataclass
class Settings:
    default_currency: str = "EUR"
    data_source: str = "yfinance"
    auto_refresh_enabled: bool = False
    auto_refresh_interval_minutes: int = 5
    last_portfolio_path: str = ""
    chart_preferences: ChartPreferences = field(default_factory=ChartPreferences)
    window_geometry: WindowGeometry = field(default_factory=WindowGeometry)
```

#### demo_portfolio.csv Format (ETFPosition Dataclass):
CSV columns: Ticker, Name, Quantity, BuyPrice, BuyDate
```python
@dataclass
class ETFPosition:
    ticker: str              # e.g., "EWLD.PA"
    name: str               # e.g., "Amundi MSCI World UCITS ETF"
    quantity: float         # e.g., 100.0
    buy_price: float        # e.g., 28.50
    buy_date: date          # IMPORTANT: Parse from "2024-01-15" to datetime.date
```

### AI_CODING_RULES.md Key Requirements for Phase 2

**MUST Requirements:**
- **C-5 (MUST):** Type hints on ALL function signatures
- **C-6 (MUST):** Use `from typing import` for complex types
- **C-8 (MUST):** Use dataclasses for configuration objects (not dicts)
- **C-10 (MUST):** Follow PEP 8 naming: snake_case functions, PascalCase classes, UPPER_SNAKE_CASE constants
- **C-12 (MUST):** Use context managers for file operations (with statement)
- **E-1 (MUST):** Specific exception types, never bare except
- **F-1 (MUST):** Use pathlib.Path for file operations, never string concatenation
- **F-2 (MUST):** Use json.load/json.dump with proper error handling
- **F-3 (SHOULD):** Validate loaded configuration against schema
- **F-4 (MUST):** Provide sensible defaults when config missing/corrupted
- **L-1 (SHOULD):** Use logging module, not print()
- **D-1 (MUST):** Every public function must have Google/NumPy style docstring

**Testing Requirements:**
- **T-1 (MUST):** Tests in tests/ directory with naming test_*.py
- **T-7 (MUST):** Use pytest as testing framework
- **T-8 (SHOULD):** Use pytest.mark.parametrize for multiple inputs
- **T-9 (MUST):** Descriptive test names that describe what's being tested
- **T-10 (SHOULD):** Use pytest fixtures for setup/teardown

### Implementation Recommendations by Module

#### config/settings.py
**Responsibilities:**
- Load/save settings from ~/Library/Application Support/PEA_ETF_Tracker/config.json
- Provide sensible defaults on missing/corrupted files
- Manage nested dataclasses (ChartPreferences, WindowGeometry)

**Key Functions:**
- `create_default_settings() -> Settings`
- `load_settings(config_path: Path = CONFIG_FILE) -> Settings` - graceful fallback to defaults
- `save_settings(settings: Settings, config_path: Path = CONFIG_FILE) -> None`
- `_validate_settings(settings_dict: Dict[str, Any]) -> bool` - private helper

**Error Handling Strategy:**
- FileNotFoundError: Create defaults, log warning
- json.JSONDecodeError: Return defaults, log error
- PermissionError: Return defaults, log error
- All other exceptions: Return defaults, log error with exc_info=True

#### data/portfolio.py
**Responsibilities:**
- Define ETFPosition dataclass with proper typing
- Implement Portfolio class with CRUD operations
- Support CSV import/export via pandas
- Support JSON persistence with ISO date format

**Key Functions:**
- `ETFPosition` dataclass with fields: ticker, name, quantity, buy_price, buy_date
- `Portfolio.__init__(positions: Optional[List[ETFPosition]] = None)`
- `Portfolio.add_position(position: ETFPosition) -> None` - validates, replaces existing ticker
- `Portfolio.remove_position(ticker: str) -> None` - raises ValueError if not found
- `Portfolio.update_position(ticker: str, position: ETFPosition) -> None`
- `Portfolio.get_position(ticker: str) -> Optional[ETFPosition]`
- `Portfolio.save_to_json(file_path: Path) -> None` - uses .isoformat() for dates
- `Portfolio.load_from_json(file_path: Path) -> Portfolio` - uses date.fromisoformat()
- `Portfolio.save_to_csv(file_path: Path) -> None` - uses pandas DataFrame
- `Portfolio.load_from_csv(file_path: Path) -> Portfolio` - validates column names

**Important Details:**
- Dates MUST be datetime.date objects, not strings
- CSV export/import uses pandas
- JSON uses ISO date format (YYYY-MM-DD)
- All file operations use context managers
- Validation: quantity > 0, buy_price > 0, ticker/name non-empty

#### data/market_data.py
**Responsibilities:**
- Fetch current prices from yfinance
- Cache prices to JSON with timestamp
- Provide fallback to cache on network failure
- Fetch historical data for analysis

**Key Functions:**
- `fetch_price(ticker: str, use_cache: bool = True) -> Optional[float]` - fallback to cache on error
- `fetch_historical_data(ticker: str, period: str = "1y") -> Optional[pd.DataFrame]`
- `save_price_to_cache(ticker: str, price: float) -> None`
- `_get_cached_price(ticker: str) -> Optional[float]`
- `_is_cache_stale(ticker: str, max_age_hours: int = 24) -> bool`
- `clear_old_cache_entries(max_age_days: int = 30) -> None`

**Cache File Location:**
```python
CACHE_DIR = Path.home() / "Library/Application Support/PEA_ETF_Tracker/cache"
PRICE_CACHE_FILE = CACHE_DIR / "price_cache.json"
```

**Cache Format:**
```json
{
  "EWLD.PA": {
    "price": 28.50,
    "timestamp": "2025-11-08T18:30:45.123456"
  }
}
```

### Testing Strategy

**test_settings.py:**
- Test dataclass construction with defaults
- Test load_settings creates file if missing
- Test load_settings reads existing file
- Test load_settings returns defaults on invalid JSON
- Test load_settings returns defaults on missing required keys
- Test save_settings creates directory if needed
- Test save_settings persists values correctly
- Use parametrize for different currencies
- Use tmp_path fixture for temp files

**test_portfolio.py:**
- Test ETFPosition creation and field types
- Test Portfolio empty initialization
- Test Portfolio initialization with positions
- Test add_position (valid, duplicate ticker replacement, validation errors)
- Test remove_position (existing, missing ticker)
- Test update_position (valid, missing ticker)
- Test get_position (found, not found)
- Test save_to_json (file created, proper format)
- Test load_from_json (reads correctly, parses dates)
- Test save_to_csv (exports correct format, uses DataFrame)
- Test load_from_csv (imports correctly, validates columns)
- Use parametrize for multiple tickers
- Test error cases (missing files, invalid data)

**test_market_data.py:**
- Test fetch_price with mocked yfinance
- Test fetch_price fallback to cache on error
- Test fetch_historical_data returns DataFrame
- Test fetch_historical_data returns None on error
- Test save_price_to_cache creates file
- Test _get_cached_price retrieves price
- Test _is_cache_stale checks age correctly
- Test clear_old_cache_entries removes old entries
- Note: May need to mock yfinance to avoid network calls

### Quality Gates for Phase 2

Before committing Phase 2 code, MUST pass all:

```bash
# 1. Code formatting
black config/ data/ tests/

# 2. Linting (MUST score ≥ 8.0 each)
pylint config/settings.py
pylint data/portfolio.py  
pylint data/market_data.py

# 3. Type checking (MUST show no errors)
mypy config/settings.py
mypy data/portfolio.py
mypy data/market_data.py

# 4. All tests passing with >80% coverage
pytest tests/test_settings.py tests/test_portfolio.py tests/test_market_data.py -v
pytest tests/ --cov=config --cov=data --cov-report=term-missing

# 5. No uncommitted changes
git status
```

### Import Order Pattern (Consistent Across All Modules)

```python
# 1. Standard library imports
import json
import logging
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# 2. Third-party imports
import pandas as pd
import numpy as np
import yfinance as yf

# 3. Local imports
from config.settings import Settings
```

### Common Pitfalls to Avoid

1. **❌ Using dict instead of @dataclass for Settings** - Use dataclass (C-8)
2. **❌ Missing type hints on functions** - Every parameter and return must have type (C-5)
3. **❌ Using print() instead of logging** - Use logging module (L-1)
4. **❌ Bare except clause** - Use specific exception types (E-1)
5. **❌ Not using context managers for files** - Always use `with` statement (C-12)
6. **❌ Hardcoding file paths as strings** - Use pathlib.Path (F-1)
7. **❌ No error handling for corrupted JSON** - Always provide defaults (F-4)
8. **❌ Tests without descriptive names** - Use descriptive test names (T-9)
9. **❌ Missing docstrings** - Every public function needs docstring (D-1)
10. **❌ Keeping BuyDate as string** - Must parse to datetime.date object

### Files to Create

Phase 2 requires creating exactly 6 new files:

1. `/Users/philippe/Documents/ETF Manager/config/settings.py` (~180 lines)
2. `/Users/philippe/Documents/ETF Manager/data/portfolio.py` (~350 lines)
3. `/Users/philippe/Documents/ETF Manager/data/market_data.py` (~220 lines)
4. `/Users/philippe/Documents/ETF Manager/tests/test_settings.py` (~150 lines)
5. `/Users/philippe/Documents/ETF Manager/tests/test_portfolio.py` (~200+ lines)
6. `/Users/philippe/Documents/ETF Manager/tests/test_market_data.py` (~200+ lines)

**Total Code:** ~1,300 lines across 6 files

### Estimated Timeline

- config/settings.py: 30-45 minutes
- data/portfolio.py: 45-60 minutes
- data/market_data.py: 45-60 minutes
- tests/test_settings.py: 30-45 minutes
- tests/test_portfolio.py: 45-60 minutes
- tests/test_market_data.py: 45-60 minutes
- Quality gates & commit: 20-30 minutes

**Total: 4-6 hours for complete Phase 2 implementation**

---

