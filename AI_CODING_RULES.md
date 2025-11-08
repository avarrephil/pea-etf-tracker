# Python AI Code Guidelines - Project By Philippe Avarre

## Implementation Best Practices

### 0 — Purpose

These rules ensure maintainability, safety, and developer velocity for Python projects.
**MUST** rules are critical; **SHOULD** rules are strongly recommended.

---

### 1 — Before Coding

- **BP-1 (MUST)** Ask the user clarifying questions.
- **BP-2 (SHOULD)** Draft and confirm an approach for complex work.
- **BP-3 (SHOULD)** If ≥ 2 approaches exist, list clear pros and cons.

---

### 2 — While Coding

- **C-1 (MUST)** Follow TDD: scaffold stub → write failing test → implement.
- **C-2 (MUST)** Name functions with existing domain vocabulary for consistency (e.g., `compute_mandelbrot`, not `calc_fractal`).
- **C-3 (SHOULD NOT)** Introduce classes when small testable functions suffice.
- **C-4 (SHOULD)** Prefer simple, composable, testable functions.
- **C-5 (MUST)** Use type hints for all function signatures:
  ```python
  def compute_mandelbrot(xmin: float, xmax: float, width: int, max_iter: int) -> np.ndarray:  # ✅ Good
      pass

  def compute_mandelbrot(xmin, xmax, width, max_iter):  # ❌ Bad
      pass
  ```
- **C-6 (MUST)** Use `from typing import` for complex types (Optional, Union, Dict, List, Tuple, etc.).
- **C-7 (SHOULD NOT)** Add comments except for critical caveats or mathematical formulas; rely on self-explanatory code and docstrings.
- **C-8 (SHOULD)** Use dataclasses for configuration objects instead of dictionaries:
  ```python
  from dataclasses import dataclass

  @dataclass
  class ViewConfig:  # ✅ Good
      center_x: float
      center_y: float
      zoom_level: float

  config = {"center_x": -0.5, "center_y": 0.0, "zoom_level": 1.0}  # ❌ Bad
  ```
- **C-9 (SHOULD NOT)** Extract a new function unless it will be reused elsewhere, is the only way to unit-test otherwise untestable logic, or drastically improves readability of an opaque block.
- **C-10 (MUST)** Follow PEP 8 naming conventions:
  - Functions and variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`
  - Private methods/attributes: `_leading_underscore`
- **C-11 (SHOULD)** Prefer f-strings over `.format()` or `%` formatting:
  ```python
  message = f"Zoom: {zoom_level:.1f}x"  # ✅ Good
  message = "Zoom: {:.1f}x".format(zoom_level)  # ❌ Bad
  ```
- **C-12 (MUST)** Use context managers for file operations and resources:
  ```python
  with open(filename, 'w') as f:  # ✅ Good
      json.dump(config, f)

  f = open(filename, 'w')  # ❌ Bad
  json.dump(config, f)
  f.close()
  ```

---

### 3 — Testing

- **T-1 (MUST)** Place unit tests in `tests/` directory with naming convention `test_*.py`.
- **T-2 (MUST)** For any API change, add/extend integration tests.
- **T-3 (MUST)** ALWAYS separate pure-logic unit tests from GUI-touching integration tests.
- **T-4 (SHOULD)** Prefer integration tests over heavy mocking, especially for GUI interactions.
- **T-5 (MUST)** Unit-test complex algorithms thoroughly (e.g., Mandelbrot computation, coordinate mapping).
- **T-6 (SHOULD)** Test the entire structure in one assertion if possible:
  ```python
  assert result.shape == (600, 800)  # Good

  assert result.shape[0] == 600  # Bad
  assert result.shape[1] == 800  # Bad
  ```
- **T-7 (MUST)** Use `pytest` as the testing framework.
- **T-8 (SHOULD)** Use `pytest.mark.parametrize` for testing multiple inputs:
  ```python
  @pytest.mark.parametrize("c,expected", [
      (0+0j, 100),  # In the set
      (2+2j, 1),    # Escapes immediately
      (-1+0j, 100), # In the set
  ])
  def test_mandelbrot_known_points(c, expected):
      result = mandelbrot_iteration(c, max_iter=100)
      assert result == expected
  ```
- **T-9 (MUST)** Use descriptive test function names that describe what is being tested:
  ```python
  def test_compute_mandelbrot_returns_correct_shape():  # ✅ Good
      pass

  def test_mandelbrot():  # ❌ Bad
      pass
  ```

---

### 4 — NumPy & Data Processing

- **N-1 (MUST)** Use NumPy vectorization instead of Python loops for numerical operations.
- **N-2 (SHOULD)** Use descriptive variable names for arrays:
  ```python
  iteration_counts = np.zeros((height, width))  # ✅ Good
  M = np.zeros((height, width))  # ❌ Bad (unless M is standard notation)
  ```
- **N-3 (MUST)** Specify dtype explicitly when creating arrays if not using default:
  ```python
  mask = np.zeros((height, width), dtype=bool)  # ✅ Good
  mask = np.zeros((height, width))  # ❌ Bad (defaults to float64)
  ```
- **N-4 (SHOULD)** Use boolean indexing for conditional operations:
  ```python
  Z[mask] = Z[mask]**2 + C[mask]  # ✅ Good

  for i in range(len(Z)):  # ❌ Bad
      if mask[i]:
          Z[i] = Z[i]**2 + C[i]
  ```

---

### 5 — Configuration & File Management

- **F-1 (MUST)** Use `pathlib.Path` for file path operations instead of string concatenation:
  ```python
  from pathlib import Path

  image_path = Path("images") / f"mandelbrot_{timestamp}.png"  # ✅ Good
  image_path = "images/" + f"mandelbrot_{timestamp}.png"  # ❌ Bad
  ```
- **F-2 (MUST)** Use `json.load()` / `json.dump()` with proper error handling for config files.
- **F-3 (SHOULD)** Validate loaded configuration against expected schema.
- **F-4 (MUST)** Provide sensible defaults when config is missing or corrupted.

---

### 6 — Code Organization

- **O-1 (MUST)** Keep related functionality together (computation, visualization, configuration).
- **O-2 (SHOULD)** Separate pure functions (no side effects) from functions with side effects (GUI updates, file I/O).
- **O-3 (MUST)** Module-level constants should be defined at the top after imports:
  ```python
  # Imports
  import numpy as np

  # Constants
  DEFAULT_WIDTH = 800
  DEFAULT_HEIGHT = 600
  ESCAPE_RADIUS = 2.0

  # Functions
  def compute_mandelbrot(...):
      pass
  ```

---

### 7 — Tooling Gates

- **G-1 (MUST)** All code must pass `black` formatter (or `autopep8` if using that).
- **G-2 (MUST)** All code must pass `pylint` or `flake8` linting with score ≥ 8.0/10.
- **G-3 (MUST)** All code must pass `mypy` type checking (strict mode recommended).
- **G-4 (MUST)** All tests must pass: `pytest tests/`

**Pre-commit checklist**:
```bash
# Format code
black mandelbrot.py tests/

# Lint
pylint mandelbrot.py
# or
flake8 mandelbrot.py

# Type check
mypy mandelbrot.py

# Run tests
pytest tests/
```

---

### 8 — Git

- **GH-1 (MUST)** Use Conventional Commits format: https://www.conventionalcommits.org/en/v1.0.0
  ```
  feat: add interactive zoom controls
  fix: correct coordinate mapping for high zoom levels
  docs: update README with installation instructions
  test: add integration tests for mouse controls
  refactor: extract color mapping to separate function
  perf: optimize mandelbrot computation with vectorization
  ```
- **GH-2 (SHOULD NOT)** Refer to Claude or Anthropic in commit messages.
- **GH-3 (SHOULD)** Keep commits atomic (one logical change per commit).
- **GH-4 (SHOULD)** Write descriptive commit messages explaining "why", not "what" (the diff shows "what").

---

### 9 — Documentation

- **D-1 (MUST)** Every public function must have a docstring in Google or NumPy style:
  ```python
  def compute_mandelbrot(xmin: float, xmax: float, ymin: float, ymax: float,
                         width: int, height: int, max_iter: int) -> np.ndarray:
      """
      Compute the Mandelbrot set over a rectangular region.

      Uses vectorized NumPy operations to calculate iteration counts
      for each point in the complex plane. Points that remain bounded
      (|z| <= 2) after max_iter iterations are considered in the set.

      Args:
          xmin: Minimum real coordinate
          xmax: Maximum real coordinate
          ymin: Minimum imaginary coordinate
          ymax: Maximum imaginary coordinate
          width: Number of pixels in x direction
          height: Number of pixels in y direction
          max_iter: Maximum number of iterations before considering point in set

      Returns:
          2D NumPy array of shape (height, width) containing iteration counts.
          Values range from 0 to max_iter.

      Example:
          >>> mandelbrot = compute_mandelbrot(-2.5, 1.0, -1.0, 1.0, 800, 600, 100)
          >>> mandelbrot.shape
          (600, 800)
      """
      pass
  ```
- **D-2 (SHOULD)** Include mathematical formulas in docstrings where relevant:
  ```python
  """
  Implements the Mandelbrot iteration: z_{n+1} = z_n^2 + c
  where z_0 = 0 and c is the complex coordinate being tested.
  """
  ```
- **D-3 (MUST)** Keep README.md up-to-date with installation, usage, and examples.
- **D-4 (SHOULD)** Document non-obvious algorithmic choices in comments.

---

## Writing Functions Best Practices

When evaluating whether a function you implemented is good or not, use this checklist:

1. **Readability**: Can you read the function and HONESTLY easily follow what it's doing? If yes, then stop here.
2. **Complexity**: Does the function have very high cyclomatic complexity (many nested if-else statements)? If yes, it needs refactoring.
3. **Algorithms**: Are there any standard data structures or algorithms that would make this function clearer and more robust?
4. **Parameters**: Are there any unused parameters in the function?
5. **Type safety**: Are all parameters and return values properly type-hinted?
6. **Testability**: Is the function easily testable without mocking core features? If not, can it be tested as part of integration tests?
7. **Dependencies**: Does it have any hidden untested dependencies that could be factored into arguments?
8. **Naming**: Brainstorm 3 better function names and see if the current name is the best and consistent with the rest of the codebase.
9. **Side effects**: Does the function clearly separate pure computation from side effects (I/O, GUI updates)?
10. **NumPy usage**: If processing arrays, is NumPy vectorization used instead of loops?

**IMPORTANT**: You SHOULD NOT refactor out a separate function unless there is a compelling need:
- The refactored function is used in more than one place
- The refactored function is easily unit testable while the original is not AND you can't test it any other way
- The original function is extremely hard to follow and you resort to putting comments everywhere

---

## Writing Tests Best Practices

When evaluating whether a test you've implemented is good or not, use this checklist:

1. **Parameterization**: SHOULD parameterize inputs; never embed unexplained literals like 42 or "foo" directly in tests.
2. **Real failures**: SHOULD NOT add a test unless it can fail for a real defect. Trivial asserts (e.g., `assert 2 == 2`) are forbidden.
3. **Descriptive names**: SHOULD ensure test function name states exactly what is being verified.
4. **Independent oracles**: SHOULD compare results to independent, pre-computed expectations, never to the function's output re-used as the oracle.
5. **Code quality**: SHOULD follow the same lint, type-safety, and style rules as production code.
6. **Property-based testing**: SHOULD express invariants or axioms when practical:
   ```python
   # Example: Mandelbrot set properties
   def test_mandelbrot_symmetry_across_real_axis():
       """Mandelbrot set is symmetric across the real axis."""
       result_upper = compute_mandelbrot(-2, 1, 0, 1, 800, 300, 100)
       result_lower = compute_mandelbrot(-2, 1, -1, 0, 800, 300, 100)
       np.testing.assert_array_equal(result_upper, np.flip(result_lower, axis=0))
   ```
7. **Test organization**: Tests for a function should be grouped logically, using classes or descriptive prefixes.
8. **Edge cases**: SHOULD test edge cases, realistic input, unexpected input, and boundary values.
9. **Type checking**: SHOULD NOT test conditions caught by type checker and mypy.
10. **Fixtures**: SHOULD use pytest fixtures for common setup/teardown:
    ```python
    @pytest.fixture
    def default_config():
        return {
            "resolution": {"width": 800, "height": 600},
            "max_iterations": 100,
            "color_scheme": "classic"
        }
    ```
11. **Assertion helpers**: Use NumPy's testing utilities for array comparisons:
    ```python
    np.testing.assert_array_equal(actual, expected)  # Exact equality
    np.testing.assert_allclose(actual, expected, rtol=1e-5)  # Floating point tolerance
    ```

---

## Code Organization - Project Structure

```
Mandelbrot/
├── mandelbrot.py              # Main application (computation, GUI, interaction)
├── requirements.txt           # Python dependencies
├── config.json               # User settings (auto-generated)
├── README.md                 # User documentation
├── PROJECT_PLAN.md           # Development plan
├── AI_CODING_RULES.md        # This file
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── test_computation.py   # Unit tests for Mandelbrot computation
│   ├── test_coordinates.py   # Unit tests for coordinate mapping
│   └── test_integration.py   # Integration tests for GUI
├── images/                   # Saved screenshots
└── docs/                     # Educational materials
    └── mathematical_background.md
```

---

## Remember Shortcuts

The user may invoke these shortcuts at any time.

### QNEW

When I type "qnew", this means:

```
Understand all BEST PRACTICES listed in AI_CODING_RULES.md.
Your code SHOULD ALWAYS follow these best practices.
```

### QPLAN

When I type "qplan", this means:

```
Analyze similar parts of the codebase and determine whether your plan:
- is consistent with rest of codebase
- introduces minimal changes
- reuses existing code
- follows Python best practices and patterns
```

### QCODE

When I type "qcode", this means:

```
Implement your plan and make sure your new tests pass.
Always run tests to make sure you didn't break anything else.
Always run `black` on newly created files to ensure standard formatting.
Always run `pylint` or `flake8` to make sure linting passes.
Always run `mypy` to ensure type checking passes.
Follow this order:
1. black mandelbrot.py tests/
2. pylint mandelbrot.py (or flake8)
3. mypy mandelbrot.py
4. pytest tests/
```

### QCHECK

When I type "qcheck", this means:

```
You are a SKEPTICAL senior Python engineer.
Perform this analysis for every MAJOR code change you introduced (skip minor changes):

1. AI_CODING_RULES.md checklist: Writing Functions Best Practices.
2. AI_CODING_RULES.md checklist: Writing Tests Best Practices.
3. AI_CODING_RULES.md checklist: Implementation Best Practices.
4. Verify PEP 8 compliance.
5. Verify proper type hints on all functions.
6. Verify docstrings are complete and accurate.
```

### QCHECKF

When I type "qcheckf", this means:

```
You are a SKEPTICAL senior Python engineer.
Perform this analysis for every MAJOR function you added or edited (skip minor changes):

1. AI_CODING_RULES.md checklist: Writing Functions Best Practices.
2. Verify function has proper type hints.
3. Verify function has complete docstring.
4. Verify function uses NumPy vectorization where applicable.
5. Verify function separates pure logic from side effects.
```

### QCHECKT

When I type "qcheckt", this means:

```
You are a SKEPTICAL senior Python engineer.
Perform this analysis for every MAJOR test you added or edited (skip minor changes):

1. AI_CODING_RULES.md checklist: Writing Tests Best Practices.
2. Verify test uses pytest best practices.
3. Verify test uses appropriate NumPy testing utilities.
4. Verify test name clearly describes what is being tested.
```

### QUX

When I type "qux", this means:

```
Imagine you are a human UX tester of the feature you implemented.
Output a comprehensive list of scenarios you would test, sorted by highest priority.
Consider:
- Mouse interactions (click, hover, drag)
- Keyboard shortcuts
- Settings panel interactions
- Edge cases (extreme zoom, invalid inputs)
- Performance under various conditions
- Cross-platform compatibility
```

### QGIT

When I type "qgit", this means:

```
Add all changes to staging, create a commit, and push to remote.

Follow this checklist for writing your commit message:
- MUST use Conventional Commits format: https://www.conventionalcommits.org/en/v1.0.0
- SHOULD NOT refer to Claude or Anthropic in the commit message.
- SHOULD structure commit message as:
  <type>[optional scope]: <description>
  [optional body]
  [optional footer(s)]

Commit types:
- feat: new feature (e.g., "feat: add color scheme cycling")
- fix: bug fix (e.g., "fix: correct zoom center calculation")
- docs: documentation only (e.g., "docs: update README with controls")
- test: adding or updating tests
- refactor: code change that neither fixes a bug nor adds a feature
- perf: performance improvement
- style: formatting, missing semicolons, etc (not user-facing style)
- chore: updating build tasks, package manager configs, etc

Example commit messages:
- feat: implement interactive zoom with mouse controls
- fix: prevent crash when config.json is corrupted
- docs: add mathematical background documentation
- test: add integration tests for keyboard shortcuts
- perf: optimize mandelbrot computation with vectorization
```

### QPERF

When I type "qperf", this means:

```
Analyze the performance of the current implementation:
1. Identify potential bottlenecks
2. Suggest optimizations (while maintaining code clarity)
3. Measure actual performance if possible
4. Compare against PRD targets (3s initial render, 2s zoom)
```

---

## Python-Specific Best Practices

### Error Handling

- **E-1 (MUST)** Use specific exception types, not bare `except`:
  ```python
  try:
      config = json.load(f)
  except json.JSONDecodeError as e:  # ✅ Good
      logger.error(f"Invalid JSON: {e}")
      config = get_default_config()

  except:  # ❌ Bad
      pass
  ```

- **E-2 (SHOULD)** Provide helpful error messages to users:
  ```python
  raise ValueError(f"Resolution {width}x{height} exceeds maximum 4000x4000")  # ✅ Good
  raise ValueError("Invalid resolution")  # ❌ Bad
  ```

### Logging

- **L-1 (SHOULD)** Use Python's `logging` module instead of `print()` for debugging:
  ```python
  import logging

  logger = logging.getLogger(__name__)
  logger.debug(f"Computing Mandelbrot: {width}x{height}")  # ✅ Good

  print(f"Computing Mandelbrot: {width}x{height}")  # ❌ Bad for debugging
  ```

### Virtual Environments

- **V-1 (SHOULD)** Always develop in a virtual environment (venv, conda, pipenv).
- **V-2 (MUST)** Keep `requirements.txt` up-to-date with exact versions for reproducibility:
  ```
  numpy==1.24.3
  matplotlib==3.7.1
  Pillow==9.5.0
  ```

---

*This file serves as a reference for AI assistants working on this Python project to ensure consistent code quality and adherence to project standards.*

---

## Phase 2: Dataclass & Configuration Management Patterns

### Dataclass Pattern for Configuration (C-8 Extension)

For Phase 2 and beyond, follow this pattern for ALL configuration dataclasses:

```python
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional, Dict, Any
import json
import logging

logger = logging.getLogger(__name__)

# Constants at module level
CONFIG_DIR = Path.home() / "Library/Application Support/PEA_ETF_Tracker"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Nested dataclasses first (from innermost to outermost)
@dataclass
class InnerConfig:
    """Inner configuration section."""
    field1: str = "default_value"
    field2: bool = True

@dataclass
class Settings:
    """Top-level settings with sensible defaults."""
    field_a: str = "default"
    field_b: int = 5
    nested: InnerConfig = field(default_factory=InnerConfig)
```

**Key Rules:**
1. Use `field(default_factory=...)` for mutable defaults (dataclass, list, dict)
2. Order: constants → nested dataclasses → outer dataclass
3. Every field must have a default value (ensure immutability pattern)
4. Use type hints on every field
5. Include docstring for each dataclass

### Dataclass-to-JSON Pattern (F-2, C-12)

For saving dataclasses to JSON:

```python
from dataclasses import asdict
import json

def save_config(config: Settings, path: Path) -> None:
    """Save configuration to JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w') as f:
        json.dump(asdict(config), f, indent=2, default=str)

def load_config(path: Path) -> Settings:
    """Load configuration from JSON with graceful defaults."""
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        # Reconstruct dataclass from loaded dict
        return Settings(**data)
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        logger.warning(f"Config error: {e}, using defaults")
        return Settings()
```

**Important for Dates:**
When serializing dates, use custom encoder:
```python
import json
from datetime import date

json.dump(asdict(config), f, indent=2, default=lambda o: o.isoformat() if isinstance(o, date) else str(o))
```

### DataFrame-to-Dataclass Pattern (For CSV)

When loading dataclass from CSV via pandas:

```python
from dataclasses import dataclass
from datetime import date
import pandas as pd

@dataclass
class Position:
    ticker: str
    quantity: float
    buy_date: date

# Loading from CSV
df = pd.read_csv('portfolio.csv')
positions = [
    Position(
        ticker=row['Ticker'],
        quantity=float(row['Quantity']),
        buy_date=pd.to_datetime(row['BuyDate']).date()  # String -> date
    )
    for _, row in df.iterrows()
]
```

### Error Handling for Configuration Files (E-1, F-4)

Pattern for robust config file handling:

```python
def load_settings(config_path: Path = CONFIG_FILE) -> Settings:
    """Load settings with graceful degradation to defaults."""
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not config_path.exists():
            logger.info(f"Config not found, creating defaults at {config_path}")
            save_settings(Settings(), config_path)
            return Settings()
        
        with open(config_path, 'r') as f:
            data = json.load(f)
        
        # Validate before reconstruction
        if not _validate_config(data):
            logger.error("Config validation failed, using defaults")
            return Settings()
        
        return Settings(**data)
        
    except FileNotFoundError as e:
        logger.warning(f"Config file missing: {e}")
        return Settings()
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}")
        return Settings()
    except PermissionError as e:
        logger.error(f"Permission denied: {e}")
        return Settings()
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return Settings()
```

### Validation Pattern (F-3)

Validate loaded configuration has required keys:

```python
def _validate_config(config_dict: Dict[str, Any]) -> bool:
    """Validate configuration has required top-level keys."""
    required_keys = {'field_a', 'field_b'}
    return all(key in config_dict for key in required_keys)
```

### Test Pattern for Dataclasses

Use pytest with tmp_path fixture:

```python
import pytest
from pathlib import Path
from config.settings import Settings, load_settings, save_settings

class TestSettings:
    """Test Settings dataclass and I/O."""
    
    def test_settings_has_defaults(self) -> None:
        """Settings provides sensible defaults."""
        s = Settings()
        assert s.field_a == "default"
        assert s.field_b == 5
    
    def test_load_creates_file_if_missing(self, tmp_path: Path) -> None:
        """load_settings creates file if missing."""
        config_file = tmp_path / "config.json"
        settings = load_settings(config_file)
        assert config_file.exists()
    
    def test_save_and_load_roundtrip(self, tmp_path: Path) -> None:
        """Save and load returns equivalent settings."""
        config_file = tmp_path / "config.json"
        original = Settings(field_a="custom")
        
        save_settings(original, config_file)
        loaded = load_settings(config_file)
        
        assert loaded.field_a == "custom"
```

### Summary: Phase 2 Requirements Checklist

For Phase 2 (and reusable for future phases):

- [ ] All configs are dataclasses with `@dataclass` decorator
- [ ] All dataclass fields have type hints
- [ ] All mutable defaults use `field(default_factory=...)`
- [ ] Constants are UPPER_SNAKE_CASE at module level
- [ ] Load/save functions handle all exception types specifically
- [ ] Config files created in ~/Library/Application Support/
- [ ] Defaults provided for missing/corrupted files
- [ ] All file I/O uses context managers (with statement)
- [ ] pathlib.Path used for all file paths (never strings)
- [ ] Logging used throughout (no print statements)
- [ ] All functions have complete type hints
- [ ] All functions have docstrings
- [ ] Tests use pytest fixtures (tmp_path)
- [ ] Tests parametrized for multiple inputs
- [ ] >80% test coverage achieved
- [ ] All quality gates pass (black, pylint ≥8.0, mypy)

