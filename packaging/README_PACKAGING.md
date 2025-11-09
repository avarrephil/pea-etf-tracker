# macOS Packaging Instructions

## Building the .app Bundle

### Prerequisites

1. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Ensure all dependencies installed:**
   ```bash
   pip install -r requirements.txt
   ```

### Build Process

**Method 1: Using the spec file (Recommended)**

```bash
cd "/Users/philippe/Documents/ETF Manager"
source .venv/bin/activate
pyinstaller packaging/pea_etf_tracker.spec
```

**Method 2: Generate spec file from scratch**

```bash
pyi-makespec --windowed --name="PEA ETF Tracker" main.py
# Then edit the generated spec file to add data files and hidden imports
pyinstaller "PEA ETF Tracker.spec"
```

### Output

- **Location:** `dist/PEA ETF Tracker.app`
- **Size:** ~150-200 MB (includes Python runtime, PyQt6, all dependencies)
- **Type:** Standalone macOS application bundle

### Testing the .app

**On Development Machine:**

```bash
open "dist/PEA ETF Tracker.app"
```

**On Clean macOS System:**

1. Copy `dist/PEA ETF Tracker.app` to another Mac
2. Double-click to launch
3. Verify:
   - App launches without errors
   - Can import demo_portfolio.csv
   - Can refresh prices (requires internet)
   - Can save portfolio
   - Charts display correctly
   - Settings persist after quit

### Troubleshooting

**Issue: "App is damaged and can't be opened"**

Solution (on user's Mac):
```bash
xattr -cr "/Applications/PEA ETF Tracker.app"
```

**Issue: Missing dependencies error**

Solution: Add to `hiddenimports` in spec file:
```python
hiddenimports = [
    'missing_module_name',
]
```

**Issue: App bundle too large (>500 MB)**

Solution: Add more packages to `excludes` in spec file:
```python
excludes = [
    'matplotlib',
    'scipy',
    'IPython',
]
```

**Issue: Charts not displaying**

Solution: Ensure PyQt6-WebEngine included:
```python
hiddenimports = [
    'PyQt6.QtWebEngineWidgets',
]
```

### Distribution

**Option 1: Direct Distribution**
- Compress: `zip -r "PEA ETF Tracker.zip" "dist/PEA ETF Tracker.app"`
- Share .zip file
- Users: Unzip and drag to Applications folder

**Option 2: DMG Creation (Optional)**
- Use `create-dmg` tool:
  ```bash
  brew install create-dmg
  create-dmg \
    --volname "PEA ETF Tracker" \
    --window-pos 200 120 \
    --window-size 600 400 \
    --icon-size 100 \
    --icon "PEA ETF Tracker.app" 200 190 \
    --hide-extension "PEA ETF Tracker.app" \
    --app-drop-link 400 190 \
    "PEA-ETF-Tracker-1.0.0.dmg" \
    "dist/PEA ETF Tracker.app"
  ```

### Code Signing (Optional - for public distribution)

**Requirements:**
- Apple Developer account ($99/year)
- Developer ID Application certificate

**Process:**
```bash
codesign --force --deep --sign "Developer ID Application: Your Name" \
  "dist/PEA ETF Tracker.app"
```

**Verification:**
```bash
codesign --verify --deep --strict "dist/PEA ETF Tracker.app"
spctl -a -t exec -vv "dist/PEA ETF Tracker.app"
```

### Notarization (Optional - for Gatekeeper approval)

**Required for:**
- Distribution outside Mac App Store
- Avoiding "unidentified developer" warnings

**Process:**
1. Code sign the app
2. Create zip: `ditto -c -k --keepParent "dist/PEA ETF Tracker.app" "PEA_ETF_Tracker.zip"`
3. Submit for notarization:
   ```bash
   xcrun notarytool submit "PEA_ETF_Tracker.zip" \
     --apple-id "your@email.com" \
     --team-id "TEAM_ID" \
     --password "app-specific-password"
   ```
4. Wait for approval
5. Staple ticket to app:
   ```bash
   xcrun stapler staple "dist/PEA ETF Tracker.app"
   ```

**Note:** Notarization optional for personal use. Required for public distribution to avoid Gatekeeper warnings.

## Build Checklist

- [ ] All dependencies installed
- [ ] PyInstaller installed
- [ ] Spec file configured with correct paths
- [ ] Hidden imports added for all required modules
- [ ] Excludes added to reduce bundle size
- [ ] Build completes without errors
- [ ] .app launches on development machine
- [ ] .app tested on clean macOS system
- [ ] Sample data accessible from .app
- [ ] All features functional (import, export, charts, settings)
- [ ] No console errors in Console.app
- [ ] Logs written to correct location

## Performance Optimization

**Reduce Bundle Size:**
- Exclude unused packages (matplotlib, scipy, jupyter)
- Use UPX compression (already enabled)
- Remove test files from build

**Improve Launch Time:**
- Use `--onefile` for single executable (slower) vs `--onedir` for folder (faster)
- Current setup uses `--onedir` via BUNDLE (recommended)

## Maintenance

**Update Version Number:**
1. Edit `packaging/pea_etf_tracker.spec`
2. Update `CFBundleVersion` and `CFBundleShortVersionString`
3. Rebuild

**Update Dependencies:**
```bash
pip install --upgrade -r requirements.txt
pyinstaller packaging/pea_etf_tracker.spec
```

## Known Limitations

- macOS only (PyInstaller can target macOS, Windows, Linux separately)
- Requires macOS 10.15 (Catalina) or later
- Python 3.11+ required for build
- Bundle size: 150-200 MB
- First launch may be slow (~5-10 seconds)

## Support

For PyInstaller issues:
- Documentation: https://pyinstaller.org/en/stable/
- GitHub: https://github.com/pyinstaller/pyinstaller

---

**Last Updated:** 2025-11-09
**PyInstaller Version:** 6.0+
**Target macOS:** 10.15+
