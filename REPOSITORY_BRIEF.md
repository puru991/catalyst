# Catalyst - Repository Brief

## Overview

**Catalyst** is an algorithmic trading library for cryptocurrency assets written in Python. It was developed by Enigma MPC (now known as Secret Labs/scrtlabs) and built on top of Quantopian's Zipline framework.

## Project Status

**⚠️ ARCHIVED - NO LONGER MAINTAINED**

- **Last Active Development**: End of 2018
- **Last Commit**: November 11, 2018
- **Original Repository**: `enigmampc/catalyst` (archived November 26, 2022)
- **Current Status**: Read-only, no official support

The original repository displays a deprecation notice:
> "This repo is no longer actively maintained since the end of 2018. If you wish to use this project or get support for it, there are many forks that may be more active."

## Core Features

### Trading Capabilities
- **Backtesting**: Test trading strategies against historical cryptocurrency data
  - Daily and minute resolution
  - Performance analytics and insights
- **Live Trading**: Real-time trading on major exchanges
  - Binance
  - Bitfinex
  - Bittrex
  - Poloniex

### Technical Features
- Built on the established Zipline algorithmic trading library
- Seamless transition between backtesting and live trading modes
- Integration with Python's scientific computing ecosystem:
  - Pandas DataFrames for performance statistics
  - matplotlib for visualization
  - scipy, statsmodels, sklearn for analysis
- Bitcoin price (btc_usdt) benchmark for performance comparison
- Pipeline API for data analysis
- Secure API key management (user-controlled exchange credentials)

## Architecture

### Technology Stack
- **Language**: Python 2.7, 3.4, 3.5
- **Core Dependencies**:
  - Zipline (algorithmic trading foundation)
  - pandas 0.19.2 (data structures)
  - numpy 1.14.0 (numerical computing)
  - scipy 1.0.0 (scientific computing)
  - ccxt 1.17.94 (exchange connectivity)
  - bcolz 1.2.1 (on-disk storage)
  - sqlalchemy 1.2.2 (asset database)
  - empyrical 0.2.1 (financial risk calculations)

### Key Components
- **Algorithm API**: High-level interface for strategy development
- **Data Pipeline**: Framework for computing and analyzing cross-sectional data
- **Exchange Connectors**: Integration with crypto exchanges via CCXT
- **Asset Database**: SQLAlchemy-based asset management
- **Backtesting Engine**: Historical simulation with minute/daily bars
- **Live Trading Engine**: Real-time order execution and portfolio management

## Repository Structure

```
catalyst/
├── catalyst/           # Main package
│   ├── algorithm.py   # TradingAlgorithm base class
│   ├── api.py         # Public API functions
│   ├── data/          # Data management and storage
│   ├── exchange/      # Exchange connectivity
│   ├── examples/      # Example trading strategies
│   ├── finance/       # Financial calculations
│   ├── pipeline/      # Data pipeline framework
│   └── utils/         # Utilities and helpers
├── docs/              # Documentation
├── etc/               # Configuration and requirements
├── tests/             # Test suite
└── setup.py           # Installation configuration
```

## Example Strategies Included

The repository includes several example trading algorithms:
- `buy_and_hodl.py` - Simple buy and hold strategy
- `dual_moving_average.py` - Moving average crossover
- `mean_reversion_simple.py` - Mean reversion strategy
- `rsi_profit_target.py` - RSI-based trading
- `portfolio_optimization.py` - Portfolio optimization
- `arbitrage_with_interface.py` - Cross-exchange arbitrage
- `buy_low_sell_high.py` - Simple momentum strategy

## Why It's Outdated

1. **Python Version**: Targets Python 2.7-3.5 (Python 2 EOL was January 2020)
2. **Dependencies**: Uses severely outdated packages:
   - pandas 0.19.2 (current: 2.x)
   - numpy 1.14.0 (current: 1.26.x)
   - setuptools pinned to 38.5.1 (current: 69.x)
   - Many security vulnerabilities in old dependencies
3. **Exchange APIs**: CCXT 1.17.94 is extremely outdated (current: 4.x)
4. **Zipline Foundation**: Based on Quantopian's Zipline, which is also unmaintained
5. **No Security Updates**: 6+ years without patches

## Potential Use Cases

Despite being outdated, this codebase could be valuable for:
- **Educational purposes**: Learning algorithmic trading concepts
- **Research**: Understanding crypto trading strategies from 2017-2018 era
- **Fork/Modernization**: Base for a modernized crypto trading framework
- **Historical backtesting**: Testing strategies against 2018-era market conditions

## Related Resources

- **Original Repository**: https://github.com/enigmampc/catalyst
- **Documentation**: https://enigmampc.github.io/catalyst/
- **Forum**: https://forum.catalystcrypto.io/ (likely inactive)
- **Package**: https://pypi.org/project/enigma-catalyst/
- **License**: Apache 2.0

## Recommendations

### For Users
- **Don't use in production**: Security risks and unmaintained dependencies
- **Consider alternatives**: Modern crypto trading frameworks like:
  - Freqtrade
  - Jesse
  - Backtrader with ccxt
  - QuantConnect (cloud-based)
  - Hummingbot (for market making)

### For Developers
- See `MODERNIZATION_PLAN.md` for steps to resurrect this project
- Significant effort required to modernize all dependencies
- May be easier to start fresh with modern tools while borrowing concepts

## License

Apache License 2.0 (see LICENSE file)

## Authors

- **Enigma MPC, Inc.** (original developers)
- **Quantopian** (Zipline foundation)
- Multiple open-source contributors

---

*Document created: 2025-11-13*
*Based on repository snapshot from: 2018-11-11*
