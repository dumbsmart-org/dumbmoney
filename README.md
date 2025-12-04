# dumbmoney

**dumbmoney** is a technical analysis and quantitative trading toolkit designed for retail investors. The current version provides a unified, transparent interface to fetch daily stock prices across A-shares, H-shares, and US markets by abstracting popular data packages like `massive`, `tushare`, and `akshare`, hiding their implementation complexity.

```python
from dumbmoney import fetch_daily_prices

df = fetch_daily_prices("600519.SH", "2025-01-01", "2025-06-01")
```

You get normalized OHLCV data automatically - no need to care which provider supplies it.

## ✨ Features

- 🔌 One function to fetch prices: fetch_daily_prices(symbol, start, end)
- 🌏 Multiple markets supported
  - A-shares (.SH, .SZ)
  - H-shares (.HK)
  - US stocks (.US)
- ⚙️ Automatic provider routing
  - A-shares → TuShare → AkShare
  - H-shares → TuShare → AkShare
  - US stocks → Massive → AkShare
- 📐 Unified normalized output
  - open, high, low, close, volume
- 🔁 Fallback logic
  - If one provider fails, the next takes over
- 🧩 Extensible architecture (plug in new providers)

### Important Notice

- To use `massive`/`tushare` as a provider, you need to apply for a key or token from them.
- `massive`'s free api key only supports retrieving data from the most recent two years.
- `tushare`'s free token only supports retrieving data of A-shares.
- `akshare` is free but depends on third-party data sources that may have variable reliability.

## 🏷️ Symbol Format

`dumbmoney` uses suffix-based symbol conventions:

| Market | Example Symbol |
|------|------|
| A-share | 600519.SH or 600519 |
| A-share | 000001.SZ or 000001 |
| H-share | 0700.HK |
| US | AAPL.US |

Suffixes for H-shares and US stocks are required. A-share symbols may omit suffixes; however, if they are present, they must be valid and correct.

## 📦 Installation

Install only the core:

```bash
pip install dumbmoney
```

Install with `tushare` and `massive`:

```bash
pip install "dumbmoney[tushare,massive]"
```

## 🚀 Quick Start

```python
from dumbmoney import fetch_daily_prices

df = fetch_daily_prices(
    "600519.SH",
    "2023-01-01",
    "2023-06-01",
    adjust="forward",
)

print(df.head())
```

To use the `massive` or `tushare` providers, you must set the required environment variables `MASSIVE_KEY` or `TUSHARE_TOKEN`.

## 📘 API Reference

`fetch_daily_prices(symbol, start, end, adjust="none", ...)`

Fetch normalized daily OHLCV prices.

- **Parameters**

| Name | Type | Description |
|------|------|------|
| `symbol` | `str` | Stock symbol with suffix (600519.SH, 0700.HK, AAPL.US) |
| `start` | `str` | Start time, e.g. "2025-01-01" |
| `end` | `str` | End time, e.g. "2025-12-01" |
| `adjust` | `str` | Adjustment mode, "none" \| "forward" \| "backward" |

- **Returns**

A `pandas.DataFrame` with:

| Column | Description |
|------|------|
| `open` | Opening price |
| `high` | High |
| `low` | Low |
| `close` | Close |
| `volume` | Traded volume |

Index is a `DatetimeIndex` named `date`.
