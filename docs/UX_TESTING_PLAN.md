# QUX Analysis - Phase 4 & 5 User Experience Testing

**PEA ETF Tracker - Comprehensive UX Testing Plan**

As a **human UX tester**, here's the comprehensive testing plan for the PEA ETF Tracker, sorted by priority from critical to nice-to-have.

---

## 🔴 **CRITICAL PRIORITY - Core Functionality**

### **1. Application Startup & Shutdown**
- [ ] **Cold start** - Launch app for first time, verify default settings created
- [ ] **Warm start** - Launch app second time, verify last portfolio loads
- [ ] **Missing config** - Delete config.json, verify app creates defaults gracefully
- [ ] **Corrupted config** - Corrupt config.json with invalid JSON, verify fallback to defaults
- [ ] **Corrupted portfolio** - Corrupt last portfolio JSON, verify app starts with empty portfolio
- [ ] **Window close** - Close window, verify geometry saved to settings
- [ ] **Force quit** - Kill app process, verify no data corruption on next launch
- [ ] **Multiple instances** - Try launching two instances, verify behavior (should work independently)

### **2. Portfolio File Operations**
- [ ] **New Portfolio** - Click File → New, verify confirmation dialog
- [ ] **Cancel new** - Click "No" on confirmation, verify portfolio unchanged
- [ ] **Confirm new** - Click "Yes", verify empty portfolio displayed
- [ ] **Open portfolio** - File → Open, select demo_portfolio.csv (should fail - JSON only)
- [ ] **Open portfolio JSON** - File → Open, select valid .json file
- [ ] **Open invalid JSON** - Try opening corrupted JSON, verify error message shown
- [ ] **Open missing file** - Try opening deleted file, verify error handling
- [ ] **Save new portfolio** - Create positions, save to new file
- [ ] **Save existing** - Modify portfolio, Ctrl+S, verify updates saved
- [ ] **Save As** - File → Save As, save to new location
- [ ] **Save As cancel** - Click cancel in dialog, verify no changes
- [ ] **Save to read-only location** - Try saving to /System, verify permission error message

### **3. CSV Import/Export**
- [ ] **Import CSV** - Import demo_portfolio.csv, verify 5 positions loaded
- [ ] **Import invalid CSV** - Import CSV with missing columns, verify error message
- [ ] **Import malformed CSV** - Import CSV with wrong data types, verify error message
- [ ] **Import empty CSV** - Import CSV with headers only, verify empty portfolio
- [ ] **Export CSV** - Export portfolio, open in Excel/Numbers, verify format
- [ ] **Export empty portfolio** - Export empty portfolio, verify headers-only CSV
- [ ] **Export then import** - Export → Import same file, verify round-trip integrity

### **4. Portfolio Table Display**
- [ ] **Empty portfolio** - Verify empty table shows 0 rows
- [ ] **1 position** - Add one position, verify displays correctly
- [ ] **5 positions** - Load demo portfolio, verify all 5 display
- [ ] **50 positions** - Import large portfolio, verify performance
- [ ] **Column headers** - Verify all 7 columns: Ticker, Name, Quantity, Buy Price, Current Price, P&L, P&L %
- [ ] **Number alignment** - Verify numeric columns right-aligned
- [ ] **Text alignment** - Verify text columns left-aligned
- [ ] **Missing prices** - Portfolio loaded but prices not fetched, verify "-" shown
- [ ] **Partial prices** - Some tickers have prices, some don't, verify correct display

### **5. Price Refresh**
- [ ] **Manual refresh** - Click Refresh button, verify spinner/progress indicator
- [ ] **F5 shortcut** - Press F5, verify refresh triggered
- [ ] **Successful refresh** - Verify current prices populate
- [ ] **Partial failure** - Some tickers fail (bad symbol), verify error logged, others succeed
- [ ] **Total failure** - Disconnect internet, refresh, verify cached prices used
- [ ] **No cache, no internet** - Clear cache, disconnect, verify graceful degradation
- [ ] **P&L calculation** - After refresh, verify P&L and P&L% calculated correctly
- [ ] **Positive P&L** - Verify green/positive formatting for gains
- [ ] **Negative P&L** - Verify red/negative formatting for losses
- [ ] **Zero P&L** - Current price = buy price, verify "±0.00" display

---

## 🟠 **HIGH PRIORITY - User Interactions**

### **6. Menu Bar Navigation**
- [ ] **File menu** - Click File, verify dropdown opens
- [ ] **Edit menu** - Click Edit, verify dropdown opens
- [ ] **Help menu** - Click Help, verify dropdown opens
- [ ] **Keyboard navigation** - Alt+F (File), Alt+E (Edit), Alt+H (Help) on Windows/Linux
- [ ] **Cmd shortcuts (macOS)** - Cmd+N, Cmd+O, Cmd+S, Cmd+Q
- [ ] **Menu mnemonics** - Verify underlined letters work (e.g., File → &New)
- [ ] **Disabled menu items** - If portfolio empty, verify some actions disabled
- [ ] **Menu hover** - Hover over menu items, verify tooltip/status text

### **7. Toolbar Actions**
- [ ] **Open button** - Click toolbar Open, verify file dialog
- [ ] **Save button** - Click toolbar Save, verify saves to last path
- [ ] **Refresh button** - Click toolbar Refresh, verify prices update
- [ ] **Toolbar tooltips** - Hover over each button, verify tooltip appears
- [ ] **Icon clarity** - Verify icons are recognizable (Open, Save, Refresh)
- [ ] **Toolbar disable** - Empty portfolio, verify appropriate buttons disabled

### **8. Keyboard Shortcuts**
- [ ] **Ctrl+N / Cmd+N** - New portfolio
- [ ] **Ctrl+O / Cmd+O** - Open portfolio
- [ ] **Ctrl+S / Cmd+S** - Save portfolio
- [ ] **Ctrl+Shift+S / Cmd+Shift+S** - Save As
- [ ] **F5** - Refresh prices
- [ ] **Ctrl+Q / Cmd+Q** - Quit application
- [ ] **Tab navigation** - Tab through UI elements
- [ ] **Escape** - Close dialogs
- [ ] **Enter** - Confirm dialogs

### **9. Table Interactions**
- [ ] **Click column header** - Sort by Ticker ascending
- [ ] **Click again** - Sort by Ticker descending
- [ ] **Sort by each column** - Ticker, Name, Quantity, Buy Price, Current Price, P&L, P&L %
- [ ] **Sort stability** - Verify stable sort (equal values maintain order)
- [ ] **Select row** - Click row, verify selection highlight
- [ ] **Multi-select** - Cmd+Click / Ctrl+Click multiple rows (if enabled)
- [ ] **Right-click context menu** - Verify context menu appears (if implemented)
- [ ] **Double-click row** - Verify edit dialog opens (Phase 6 feature)
- [ ] **Keyboard selection** - Arrow keys navigate rows
- [ ] **Page Up/Down** - Scroll large portfolios
- [ ] **Home/End** - Jump to first/last row

### **10. Status Bar**
- [ ] **Initial state** - App starts, verify "Ready" shown
- [ ] **After price refresh** - Verify "Portfolio Value: €X.XX | P&L: ±€X.XX"
- [ ] **Empty portfolio** - Verify status bar handles gracefully
- [ ] **Large numbers** - Portfolio value > €1,000,000, verify formatting
- [ ] **Negative P&L** - Verify minus sign displayed correctly
- [ ] **Status updates** - Verify status changes during operations (loading, saving)

---

## 🟡 **MEDIUM PRIORITY - Visual & Feedback**

### **11. Window Management**
- [ ] **Initial window size** - First launch, verify 1200x800 default
- [ ] **Window position** - First launch, verify centered on screen (100, 100)
- [ ] **Resize window** - Drag edges, verify table resizes responsively
- [ ] **Minimize window** - Minimize, restore, verify state preserved
- [ ] **Maximize window** - Maximize, verify full-screen layout
- [ ] **Restore window** - Restore from maximized, verify previous size
- [ ] **Multi-monitor** - Move window to second monitor, close, reopen, verify position saved
- [ ] **Monitor disconnect** - Disconnect monitor, reconnect, verify window still accessible
- [ ] **Very small window** - Resize to 400x300, verify UI still usable
- [ ] **Very large window** - Resize to 4K resolution, verify no layout issues

### **12. Visual Polish**
- [ ] **Table column widths** - Verify columns resize proportionally
- [ ] **Text readability** - Check font size, contrast, clarity
- [ ] **Number formatting** - Verify €2,935.00 format with commas for thousands
- [ ] **Percentage display** - Verify +2.98% format with sign
- [ ] **Alignment consistency** - Verify consistent spacing throughout
- [ ] **Color scheme** - Verify professional color palette
- [ ] **Positive/negative indicators** - Green for gains, red for losses (if implemented)
- [ ] **Row hover effect** - Hover over row, verify highlight (if implemented)
- [ ] **Selection highlight** - Selected row clearly distinguished

### **13. Dialog Interactions**
- [ ] **File Open dialog** - Verify native macOS file picker
- [ ] **File Save dialog** - Verify default location, file extension
- [ ] **Confirmation dialog** - New Portfolio, verify "Yes/No" buttons
- [ ] **Error message dialog** - Trigger error, verify clear message
- [ ] **About dialog** - Help → About, verify version, copyright
- [ ] **Dialog modality** - Verify main window blocked during dialog
- [ ] **Dialog escape** - Press Escape, verify dialog closes
- [ ] **Dialog enter** - Press Enter, verify default action triggered

### **14. Error Handling & Messages**
- [ ] **Network error** - Disconnect internet, refresh, verify user-friendly message
- [ ] **File not found** - Open deleted file, verify clear error
- [ ] **Permission denied** - Save to read-only location, verify error explanation
- [ ] **Invalid JSON** - Open corrupted file, verify specific error message
- [ ] **Invalid CSV** - Import malformed CSV, verify column validation message
- [ ] **Disk full** - Save with no disk space, verify error (hard to test)
- [ ] **Error dialog buttons** - Verify "OK" or "Cancel" always present
- [ ] **Error logging** - Check app.log for detailed error information

---

## 🟢 **LOW PRIORITY - Edge Cases & Performance**

### **15. Data Validation**
- [ ] **Empty ticker** - Portfolio with empty ticker string, verify handling
- [ ] **Very long ticker** - Ticker > 50 chars, verify display truncation
- [ ] **Special characters** - Ticker with emoji/unicode, verify display
- [ ] **Negative quantity** - Portfolio with negative shares, verify display (invalid data)
- [ ] **Zero quantity** - Position with 0 shares, verify handling
- [ ] **Negative buy price** - Invalid data, verify doesn't crash
- [ ] **Very large numbers** - 1,000,000 shares at €10,000, verify formatting
- [ ] **Very small numbers** - 0.001 shares, verify precision
- [ ] **Date formats** - Various date formats in CSV, verify parsing

### **16. Performance Testing**
- [ ] **Large portfolio (100 positions)** - Load, verify <2s
- [ ] **Large portfolio (1000 positions)** - Load, verify reasonable time
- [ ] **Price refresh (100 tickers)** - Verify progressive update or loading indicator
- [ ] **Table scrolling** - 1000 rows, verify smooth scrolling
- [ ] **Table sorting** - 1000 rows, verify instant sort
- [ ] **Window resize** - Rapid resize, verify no lag
- [ ] **Memory usage** - Run for 1 hour, verify no memory leaks
- [ ] **CPU usage** - Idle state, verify <1% CPU
- [ ] **Auto-refresh** - Enable 5-min refresh, verify no degradation over time

### **17. Settings Persistence**
- [ ] **Window geometry** - Resize, close, reopen, verify same size
- [ ] **Window position** - Move, close, reopen, verify same position
- [ ] **Last portfolio path** - Open portfolio, quit, reopen app, verify auto-loads
- [ ] **Settings file location** - Verify ~/Library/Application Support/PEA_ETF_Tracker/config.json
- [ ] **Portable settings** - Copy config to new machine, verify works
- [ ] **Settings migration** - Upgrade app version, verify old settings compatible

### **18. Concurrent Operations**
- [ ] **Save during refresh** - Start refresh, immediately save, verify no corruption
- [ ] **Close during save** - Start save, close window, verify save completes
- [ ] **Open during refresh** - Start refresh, open new portfolio, verify refresh cancels
- [ ] **Multiple file operations** - Rapid File → Open → Save → Import, verify queue handling
- [ ] **Refresh spam** - Click refresh 10 times rapidly, verify only one refresh runs

---

## 🔵 **NICE-TO-HAVE - Advanced Features**

### **19. Accessibility**
- [ ] **VoiceOver (macOS)** - Enable VoiceOver, verify navigation
- [ ] **Screen reader** - Verify menu items read aloud
- [ ] **Keyboard-only navigation** - Complete workflow without mouse
- [ ] **High contrast** - Enable macOS high contrast mode, verify readability
- [ ] **Large text** - System font size 24pt, verify UI scales
- [ ] **Color blindness** - Test with color blindness simulator

### **20. Auto-Refresh**
- [ ] **Enable auto-refresh** - Settings → Auto-refresh ON, verify timer starts
- [ ] **Auto-refresh interval** - Set 5 minutes, verify refresh every 5 min
- [ ] **Auto-refresh indicator** - Verify status bar shows "Refreshing..."
- [ ] **Disable auto-refresh** - Turn off, verify timer stops
- [ ] **Auto-refresh during operation** - Editing portfolio, auto-refresh triggers, verify no conflict
- [ ] **Auto-refresh on wake** - Sleep computer, wake, verify refresh triggers

### **21. Localization (Future)**
- [ ] **French locale** - Change system language to French, verify labels
- [ ] **German locale** - Change to German, verify translations
- [ ] **Number formatting** - EU locale (comma as decimal), verify €1.234,56
- [ ] **Date formatting** - EU format DD/MM/YYYY vs US MM/DD/YYYY
- [ ] **Currency symbol** - Verify € (euro) displays correctly

### **22. Cross-Platform (If Supported)**
- [ ] **Windows 10** - Run on Windows, verify native look-and-feel
- [ ] **Windows 11** - Verify Windows 11 styling
- [ ] **macOS Ventura** - Native macOS menus, dialogs
- [ ] **macOS Sonoma** - Latest macOS compatibility
- [ ] **Linux Ubuntu** - Verify GTK themes respected
- [ ] **File paths** - Verify cross-platform path handling (/ vs \)
- [ ] **Keyboard shortcuts** - Ctrl vs Cmd on different platforms

---

## 🎯 **Testing Scenarios - Real User Workflows**

### **Scenario 1: First-Time User**
1. Launch app for first time
2. See empty portfolio
3. File → Import CSV → demo_portfolio.csv
4. See 5 positions loaded
5. Click Refresh (F5)
6. See prices populate, P&L calculated
7. File → Save As → my_portfolio.json
8. Close app
9. Reopen app → verify my_portfolio.json auto-loads

### **Scenario 2: Daily Portfolio Check**
1. Launch app (last portfolio loads)
2. Press F5 to refresh prices
3. Check status bar for total value and P&L
4. Sort by P&L % column (best performers)
5. Note top/bottom performers
6. Close app

### **Scenario 3: Portfolio Modification**
1. Open existing portfolio
2. Notice incorrect quantity for EWLD.PA
3. Double-click row to edit (Phase 6 feature)
4. Change quantity from 100 to 150
5. Press F5 to refresh with new quantity
6. Verify new P&L calculation
7. Ctrl+S to save

### **Scenario 4: Error Recovery**
1. Launch app
2. Disconnect internet
3. Try to refresh prices
4. See error: "Could not fetch prices, using cache"
5. Verify cached prices shown
6. Reconnect internet
7. Refresh again
8. Verify fresh prices fetched

### **Scenario 5: Multi-Portfolio Management**
1. Have portfolio_A.json open
2. File → New
3. Create empty portfolio
4. File → Import CSV → portfolio_B.csv
5. Compare side-by-side (Phase 6: multiple windows)
6. File → Save As → portfolio_B.json
7. File → Open → portfolio_A.json (switch back)

---

## 📊 **Performance Benchmarks**

| Action | Target | Acceptable | Poor |
|--------|--------|------------|------|
| App launch (cold) | <2s | <5s | >5s |
| App launch (warm) | <1s | <3s | >3s |
| Load 50-position portfolio | <0.5s | <1s | >1s |
| Load 500-position portfolio | <2s | <5s | >5s |
| Refresh 10 prices | <3s | <10s | >10s |
| Refresh 50 prices | <10s | <30s | >30s |
| Save portfolio | <0.5s | <2s | >2s |
| Window resize | 60fps | 30fps | <30fps |
| Table sort (1000 rows) | <0.5s | <2s | >2s |
| CSV import (1000 rows) | <2s | <5s | >5s |

---

## 🐛 **Known Issues to Test**

1. **Network timeout** - If yfinance takes >30s, does app hang?
2. **Price data missing** - Some ETFs don't have `currentPrice`, verify fallback
3. **CSV encoding** - Test UTF-8, UTF-16, ASCII CSV files
4. **Very long portfolio names** - File paths > 255 chars
5. **Special characters in paths** - Spaces, accents, emoji in file paths
6. **Concurrent file access** - Two apps opening same portfolio.json
7. **Partial writes** - App crashes during save, verify no corruption

---

## ✅ **Test Coverage Summary**

- **Critical**: 60 scenarios - **MUST PASS**
- **High Priority**: 45 scenarios - Should pass before release
- **Medium Priority**: 35 scenarios - Nice to have
- **Low Priority**: 30 scenarios - Future enhancements
- **Total**: **170 UX test scenarios**

---

## 🎯 **Priority for Phase 4 & 5 Testing**

### **Must Test Before Release:**
1. ✅ All file operations (New, Open, Save, Import, Export)
2. ✅ Price refresh and P&L calculation accuracy
3. ✅ Table display, sorting, and interaction
4. ✅ Keyboard shortcuts (Ctrl+S, F5, Ctrl+Q)
5. ✅ Error handling (network, file not found, corrupted data)
6. ✅ Window geometry persistence
7. ⚠️ Performance with 100+ positions
8. ⚠️ Auto-refresh (Phase 5 implemented but needs extensive testing)

### **Next Phase (Phase 6) Features:**
- Add/Edit/Delete position dialogs
- Charts tab with Plotly embedding
- Settings dialog for preferences
- Context menus for table rows
- Enhanced visual feedback (loading spinners, progress bars)
- Color coding for positive/negative P&L
- Row hover effects
- Multi-selection support

---

## 📝 **Testing Notes**

### **Test Environment:**
- macOS Sonoma (primary target)
- Python 3.12+
- PyQt6 6.6.1
- Sample data: demo_portfolio.csv (5 positions)

### **Test Data Files:**
- `sample_data/demo_portfolio.csv` - Valid 5-position portfolio
- `sample_data/demo_config.json` - Default configuration
- `sample_data/sample_etfs.json` - 10 common PEA ETFs

### **Log Files:**
- Application log: `~/Library/Logs/PEA_ETF_Tracker/app.log`
- Settings: `~/Library/Application Support/PEA_ETF_Tracker/config.json`
- Price cache: `~/Library/Application Support/PEA_ETF_Tracker/cache/prices.json`

---

## 🚀 **Regression Testing Checklist**

After any code changes, run these critical tests:

1. [ ] Launch app (cold start)
2. [ ] Import demo_portfolio.csv
3. [ ] Refresh prices (F5)
4. [ ] Verify P&L calculated
5. [ ] Save portfolio
6. [ ] Close and reopen app
7. [ ] Verify last portfolio loads
8. [ ] Sort table by P&L %
9. [ ] Export to CSV
10. [ ] Verify all 140 pytest tests pass

---

**Document Version:** 1.0
**Last Updated:** 2025-01-08
**Phase:** 4 & 5 Complete
**Status:** Ready for User Acceptance Testing
