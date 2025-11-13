# Catalyst Modernization Plan

## Executive Summary

This document outlines the steps required to modernize the Catalyst cryptocurrency algorithmic trading library from its 2018 codebase to a functional, secure, and maintainable state in 2025. This is a **significant undertaking** requiring 200+ hours of development effort.

**Recommendation**: Consider using modern alternatives (Freqtrade, Jesse, etc.) unless you have specific reasons to resurrect this codebase.

## Current State Assessment

### Critical Issues
- ❌ Python 2.7 compatibility code (EOL since January 2020)
- ❌ Python 3.4/3.5 only (current: 3.12)
- ❌ pandas 0.19.2 (current: 2.x) - breaking API changes
- ❌ numpy 1.14.0 (current: 1.26.x) - breaking API changes
- ❌ CCXT 1.17.94 (current: 4.x) - completely rewritten API
- ❌ Dozens of security vulnerabilities in dependencies
- ❌ Cython extensions need recompilation for modern Python
- ❌ Zipline foundation also unmaintained

### Architecture Challenges
- Heavy reliance on outdated Zipline internals
- Tight coupling with specific pandas/numpy versions
- Custom Cython extensions throughout codebase
- Exchange APIs may have changed significantly since 2018

## Modernization Phases

---

## Phase 1: Environment Setup & Assessment (10-15 hours)

### 1.1 Create Isolated Development Environment

```bash
# Create Python 3.11 virtual environment (3.12 may have issues with older packages)
python3.11 -m venv catalyst-dev
source catalyst-dev/bin/activate

# Install build tools
pip install --upgrade pip setuptools wheel cython
```

### 1.2 Attempt Baseline Installation

```bash
# This will likely fail - document all errors
pip install -e .
```

**Expected Issues**:
- setuptools version conflicts
- Cython compilation failures
- Incompatible numpy/pandas versions
- Missing or incompatible dependencies

### 1.3 Create Compatibility Matrix

Document which dependencies can be upgraded without code changes:
- Safe upgrades (no API changes)
- Minor code changes needed
- Major refactoring required
- Complete replacement needed

---

## Phase 2: Dependency Modernization (40-60 hours)

### 2.1 Update Core Scientific Stack

**Priority: CRITICAL**

Current → Target:
- `numpy==1.14.0` → `numpy>=1.24.0,<2.0`
- `pandas==0.19.2` → `pandas>=2.0.0`
- `scipy==1.0.0` → `scipy>=1.11.0`

**Required Code Changes**:

#### pandas API Changes
```python
# Old (pandas 0.19):
df.sort(['column'])
df.ix[row, col]
Panel() objects

# New (pandas 2.x):
df.sort_values('column')
df.loc[row, col]
# Panel removed - refactor to MultiIndex DataFrame
```

#### numpy API Changes
```python
# Old:
np.float
np.int

# New:
np.float64
np.int64
```

**Affected Files** (estimate):
- `catalyst/data/*.py` (~20 files)
- `catalyst/finance/*.py` (~15 files)
- `catalyst/pipeline/*.py` (~30 files)

### 2.2 Update Exchange Connectivity

**Priority: CRITICAL**

Current → Target:
- `ccxt==1.17.94` → `ccxt>=4.0.0`

**Challenges**:
- CCXT API completely redesigned between v1 and v4
- Exchange endpoints changed
- Authentication methods updated
- Many exchanges from 2018 no longer exist

**Strategy**:
1. Audit all CCXT usage in codebase
2. Create compatibility layer for old API
3. Gradually migrate to new CCXT patterns
4. Remove support for defunct exchanges

**Affected Files**:
- `catalyst/exchange/*.py` (entire directory)
- `catalyst/data/bundles/*.py`

### 2.3 Update Build System

Current → Target:
- `setuptools==38.5.1` → `setuptools>=69.0.0`
- `Cython==0.27.3` → `Cython>=3.0.0`

**Required Changes**:
1. Rewrite Cython extensions for Cython 3.x compatibility
2. Update `setup.py` to modern setuptools API
3. Consider migrating to `pyproject.toml` (PEP 517/518)
4. Update numpy C-API usage in Cython code

**Files to Update**:
- `setup.py`
- All `.pyx` files (10+ files)
- All `.pxd` files (header files)

### 2.4 Replace/Update Other Dependencies

| Package | Current | Target | Effort |
|---------|---------|--------|--------|
| python-dateutil | 2.7.3 | >=2.8.0 | Low |
| requests | 2.20.1 | >=2.31.0 | Low |
| sqlalchemy | 1.2.2 | >=2.0.0 | Medium |
| alembic | 0.9.7 | >=1.13.0 | Medium |
| bcolz | 1.2.1 | ? (unmaintained) | High |
| tables | 3.4.2 | >=3.9.0 | Medium |
| networkx | 2.1 | >=3.0 | Medium |
| statsmodels | 0.8.0 | >=0.14.0 | Medium |

**Critical Decision: bcolz**
- bcolz is unmaintained (like Catalyst)
- Options:
  1. Fork and maintain bcolz
  2. Replace with alternatives (zarr, parquet, HDF5)
  3. Keep old version in isolated environment

---

## Phase 3: Python 3 Compatibility (20-30 hours)

### 3.1 Remove Python 2 Support

**Tasks**:
1. Remove `from __future__ import` statements (or keep for clarity)
2. Update print statements: `print x` → `print(x)`
3. Update exception syntax: `except Error, e:` → `except Error as e:`
4. Fix integer division: ensure `/` vs `//` is correct
5. Update string/bytes handling
6. Remove `six` library usage (or keep for compatibility)

**Tools**:
```bash
# Automated detection
pip install pyupgrade
find catalyst -name "*.py" -exec pyupgrade --py311-plus {} \;

# Check for issues
pip install pylint
pylint catalyst --py-version=3.11
```

### 3.2 Update Type Annotations

Add modern type hints for better code quality:
```python
# Old:
def process_data(data):
    return data.mean()

# New:
from typing import Union
import pandas as pd
import numpy as np

def process_data(data: Union[pd.DataFrame, np.ndarray]) -> float:
    return data.mean()
```

---

## Phase 4: Fix Cython Extensions (30-40 hours)

### 4.1 Audit All Cython Code

**Files**:
- `catalyst/assets/_assets.pyx`
- `catalyst/lib/adjustment.pyx`
- `catalyst/lib/_factorize.pyx`
- `catalyst/lib/*window.pyx` (multiple files)
- `catalyst/lib/rank.pyx`
- `catalyst/data/_equities.pyx`
- `catalyst/data/_adjustments.pyx`
- `catalyst/_protocol.pyx`
- `catalyst/gens/sim_engine.pyx`
- `catalyst/data/_minute_bar_internal.pyx`
- `catalyst/utils/calendars/_calendar_helpers.pyx`
- `catalyst/data/_resample.pyx`

### 4.2 Update for Cython 3.x

**Common Issues**:
- `np.float_` → `np.float64`
- `np.int_` → `np.int64`
- Updated numpy C-API
- Changed GIL acquisition syntax
- Updated exception handling

### 4.3 Recompile and Test

```bash
# Clean old builds
python setup.py clean --all
rm -rf build/ dist/ *.egg-info

# Rebuild extensions
python setup.py build_ext --inplace

# Test each extension
python -c "import catalyst.lib._factorize"
# ... repeat for all extensions
```

---

## Phase 5: Exchange Integration Update (40-50 hours)

### 5.1 Audit Current Exchange Support

**2018 Exchanges**:
- ✅ Binance (still active, API changed)
- ✅ Bitfinex (still active, API changed)
- ❌ Bittrex (API changed, less relevant)
- ❌ Poloniex (ownership changed, less relevant)

### 5.2 Update CCXT Integration

**Old Pattern** (CCXT 1.x):
```python
exchange = ccxt.binance({
    'apiKey': key,
    'secret': secret,
})
markets = exchange.load_markets()
ticker = exchange.fetch_ticker('BTC/USDT')
```

**New Pattern** (CCXT 4.x):
```python
exchange = ccxt.binance({
    'apiKey': key,
    'secret': secret,
    'enableRateLimit': True,
})
await exchange.load_markets()
ticker = await exchange.fetch_ticker('BTC/USDT')
# Note: async/await required in v4
```

### 5.3 Add Async Support

CCXT 4.x is async-first, requiring major refactoring:
1. Convert exchange calls to async/await
2. Update algorithm execution to handle async
3. Add asyncio event loop management
4. Handle rate limiting properly

### 5.4 Test Live Trading

**WARNING**: Use testnet/paper trading only!

---

## Phase 6: Testing & Validation (30-40 hours)

### 6.1 Fix Existing Tests

```bash
# Run test suite
pytest tests/

# Expected: Many failures
# Tasks:
# 1. Update test fixtures for new pandas/numpy
# 2. Fix mocking for new library versions
# 3. Update expected outputs
# 4. Add new tests for modernized code
```

### 6.2 Create Integration Tests

Test critical paths:
- Data ingestion from exchanges
- Backtesting with historical data
- Order execution (paper trading)
- Performance calculations
- Portfolio management

### 6.3 Validate Backtesting Results

Compare old vs new implementation:
- Same strategy should produce similar results
- Account for any intentional changes
- Document breaking changes

---

## Phase 7: Documentation Update (15-20 hours)

### 7.1 Update Installation Instructions

```markdown
# Old:
pip install enigma-catalyst

# New:
git clone https://github.com/yourusername/catalyst
cd catalyst
pip install -e .
```

### 7.2 Update API Documentation

- Mark deprecated features
- Document new requirements (Python 3.11+)
- Update exchange-specific docs
- Add migration guide from old version

### 7.3 Update Examples

All example strategies need updates:
- New pandas API
- New CCXT patterns
- Modern Python idioms

---

## Phase 8: Security & Performance (20-30 hours)

### 8.1 Security Audit

Run security scanners:
```bash
pip install safety bandit
safety check
bandit -r catalyst/
```

Fix:
- SQL injection vulnerabilities
- Insecure API key storage
- Outdated crypto libraries
- Dependency vulnerabilities

### 8.2 Performance Optimization

- Profile slow operations
- Optimize data loading
- Cache expensive computations
- Consider alternatives to bcolz

### 8.3 Add Modern DevOps

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: pip install -e .[dev]
      - name: Run tests
        run: pytest tests/
```

---

## Alternative Approach: Minimal Viable Version

If full modernization is too ambitious, create a minimal working version:

### Quick Start (10-20 hours)

1. **Use Docker with Python 3.5**:
   ```dockerfile
   FROM python:3.5-slim
   RUN apt-get update && apt-get install -y gcc g++ make
   COPY . /catalyst
   WORKDIR /catalyst
   RUN pip install -e .
   ```

2. **Pin All Dependencies**: Keep everything at 2018 versions

3. **Isolation**: Run in completely isolated environment

4. **Read-Only**: Use for backtesting historical data only

5. **No Live Trading**: Security risks too high

### Pros:
- Fast to set up
- Minimal code changes
- Can study/learn from code

### Cons:
- Security vulnerabilities
- No new features
- Limited to Python 3.5
- Cannot use with modern data sources

---

## Resource Requirements

### Time Estimates

| Phase | Hours | Difficulty |
|-------|-------|------------|
| 1. Environment Setup | 10-15 | Easy |
| 2. Dependencies | 40-60 | Hard |
| 3. Python 3 Compat | 20-30 | Medium |
| 4. Cython Extensions | 30-40 | Hard |
| 5. Exchange Integration | 40-50 | Hard |
| 6. Testing | 30-40 | Medium |
| 7. Documentation | 15-20 | Easy |
| 8. Security/Performance | 20-30 | Medium |
| **TOTAL** | **205-285** | **Hard** |

### Skills Required

- **Essential**:
  - Advanced Python (2.x → 3.x migration)
  - pandas/numpy internals
  - Cython programming
  - Exchange APIs and trading concepts
  - Git/version control

- **Helpful**:
  - Financial markets knowledge
  - DevOps/CI-CD
  - Security best practices
  - Async programming

### Tools Needed

- Python 3.11 (or 3.10)
- C/C++ compiler (for Cython)
- Git
- IDE with Python support
- Exchange API accounts (for testing)
- Significant computing resources (for backtesting)

---

## Decision Matrix: Should You Modernize?

### ✅ Proceed if:
- You need specific Catalyst features not available elsewhere
- You have 200+ hours of developer time
- You have strong Python/Cython expertise
- You need to maintain an existing Catalyst deployment
- This is a learning exercise

### ❌ Use Alternatives if:
- You want to trade crypto algorithmically (use Freqtrade, Jesse, etc.)
- You're new to algorithmic trading
- Time is limited
- You need production-ready software
- You need active community support

---

## Recommended Modern Alternatives

### 1. Freqtrade
- **Pros**: Active development, modern Python, great docs, large community
- **Focus**: Crypto trading with machine learning
- **URL**: https://github.com/freqtrade/freqtrade

### 2. Jesse
- **Pros**: Modern design, clean API, good backtesting
- **Focus**: Cryptocurrency algorithmic trading
- **URL**: https://jesse.trade/

### 3. Backtrader
- **Pros**: Mature, flexible, good docs
- **Cons**: More complex API
- **URL**: https://www.backtrader.com/

### 4. QuantConnect LEAN
- **Pros**: Multi-asset, cloud platform, modern C#/Python
- **Cons**: Cloud-dependent for some features
- **URL**: https://github.com/QuantConnect/Lean

### 5. VectorBT
- **Pros**: Fast backtesting, modern Python, NumPy-based
- **Focus**: Vectorized backtesting
- **URL**: https://github.com/polakowo/vectorbt

---

## Conclusion

Modernizing Catalyst is **technically feasible** but requires **significant effort**. For most use cases, modern alternatives will be faster, safer, and more maintainable.

**Recommendation**:
- Use Catalyst code as **reference/learning material**
- Build with modern frameworks (Freqtrade, Jesse)
- Port specific strategies to new platforms
- Avoid full modernization unless absolutely necessary

---

## Quick Start Commands (For the Brave)

```bash
# 1. Clone repository
git clone https://github.com/yourusername/catalyst
cd catalyst

# 2. Create virtual environment (Python 3.11)
python3.11 -m venv venv
source venv/bin/activate

# 3. Install build dependencies
pip install --upgrade pip setuptools wheel
pip install cython numpy

# 4. Try to install (will likely fail)
pip install -e .

# 5. Document errors and start Phase 2
# Good luck! You'll need it.
```

---

*Document created: 2025-11-13*
*Estimated effort: 200-285 hours of experienced developer time*
*Complexity: High*
*Recommendation: Consider alternatives unless specific requirements demand Catalyst*
