import pandas as pd

from typing import Optional, Mapping, Tuple, Any

from .base import BaseChart
from .mplfinance import MPLFinanceChart


def get_backend(name: str) -> BaseChart:
  """Get chart backend by name."""
  name = name.lower()
  if name in ("mpl", "mplfinance"):
    return MPLFinanceChart()
  if name == "plotly":
    from .plotly import PlotlyChart
    return PlotlyChart()
  raise ValueError(f"Unknown chart backend: {name}")

def plot_kline(
  data: pd.DataFrame,
  backend: str = "mplfinance",
  indicators: Optional[Mapping[str, pd.Series]] = None,
  volume: Optional[bool] = None,
  title: Optional[str] = None,
  **kwargs,
) -> Tuple[Any, ...]:
  """
  Convenience function to plot K-line chart using specified backend.
  """
  bk = get_backend(backend)
  return bk.plot_kline(
    data=data,
    indicators=indicators,
    volume=volume,
    title=title,
    **kwargs,
  )