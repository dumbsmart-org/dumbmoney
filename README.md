# dumbmoney

**dumbmoney** is a technical analysis and quantitative trading toolkit designed for retail investors. The current version provides a unified, transparent interface to fetch daily stock prices across A-shares, H-shares, and US markets by abstracting popular data packages like `massive`, `tushare`, and `akshare`, hiding their implementation complexity.

*To use the `massive` or `tushare` providers, you must set the required environment variables `MASSIVE_KEY` or `TUSHARE_TOKEN`.*

## 📦 Installation

Install only the core:

```bash
pip install dumbmoney
```

## 🚀 Quick Start

```python
from dumbmoney import fetch_daily_prices, plot_kline

os.environ["TUSHARE_TOKEN"] = "xxxxxx"
os.environ["MASSIVE_KEY"] = "yyyyyy"

df = fetch_daily_prices("AAPL.US", "2025-06-01")
print(df.tail())

fig, _ = plot_kline(df, title="AAPL Daily K-Line Chart")

from matplotlib import pyplot as plt
plt.show()

ifig = plot_kline(df, backend="plotly", title="AAPL Daily K-Line Chart (Plotly)")
ifig.show()
```

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

- `massive`'s free api key only supports retrieving data of US stocks from the most recent two years.
- `tushare`'s free token only supports retrieving data of A-shares.
- `akshare` is free but depends on third-party data sources that may have variable reliability.

## 🏷️ Symbol Format

`dumbmoney` uses suffix-based symbol conventions:

| Market | Example Symbol |
|------|------|
| SH | 600519.SH or 600519 |
| SZ | 000001.SZ or 000001 |
| KCB | 688235.SH or 688235 |
| ETF_SH | 513090.SH or 513090, 562500.SH or 562500, 588080.SH or 588080 |
| ETF_SZ | 159652.SZ or 159652 |
| HK | 0700.HK |
| US | AAPL.US |

Suffixes for H-shares and US stocks are required. A-share symbols may omit suffixes; however, if they are present, they must be valid and correct.

## 📘 API Reference

### `fetch_daily_prices(symbol, start, end, adjust="none")`

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

### `plot_kline(data, backend="mpl", indicators=None, volume=None, title=None, **kwargs)`

Plot k-line (candlestick) chart using the provided `DataFrame` data.

- **Parameters**

| Name | Type | Description |
|------|------|------|
| `data` | `pandas.DataFrame`| DataFrame containing OHLCV columns (`open`, `high`, `low`, `close`, `volume`) |
| `backend` | `str` | Charting backend to use. Currently support `"mpl"` (mplfinance) and `"plotly"` (plotly). |
| `indicators` | `list` or `None` | List of technical indicators to overlay (for future implementation). Default is `None`. |
| `volume` | `bool` or `None` | Whether to plot volume below the k-line chart. Default is `None` (auto-detect). |
| `title` | `str` or `None` | Chart title. Default is `None`. |
| `**kwargs` | - | Additional keyword arguments passed to the plotting backend. |

- **Returns**

A tuple `(fig, ax)` where:

| Name | Type | Description |
|------|------|------|
| `fig` | `matplotlib.figure.Figure` | The matplotlib Figure object for the chart. |
| `ax`  | `matplotlib.axes.Axes` | The main Axes object for the k-line chart. |
