from typing import Any, Mapping, Optional

import pandas as pd

from .base import BaseChart, OHLCData


class MPLFinanceChart(BaseChart):
  """Chart implementation using mplfinance."""
  
  def __init__(self, default_volume: bool = True, style: str = "yahoo"):
    super().__init__(default_volume=default_volume)
    self.style = style
  
  def _plot_kline(
    self,
    ohlc: OHLCData,
    indicators: Optional[Mapping[str, pd.Series]] = None,
    volume: bool = True,
    title: Optional[str] = None,
    **kwargs
  ) -> Any:
    try:
      import mplfinance as mpf
    except ImportError:
      raise ImportError("mplfinance is not installed.")
    
    df = ohlc  # type: ignore[assignment]
    
    addplots = []
    if indicators:
      for name, series in indicators.items():
        s = series.reindex(df.index)
        ap = mpf.make_addplot(s, panel=0, ylabel=name)
        addplots.append(ap)
        
    has_volume = volume and "volume" in df.columns
    
    mpf_kwargs = {
      "type": "candle",
      "style": self.style,
      "title": title or "Price (K-line) Chart",
      "volume": has_volume,
      "addplot": addplots if addplots else [],
      "returnfig": True
    }
    mpf_kwargs.update(kwargs)
    
    fig, ax = mpf.plot(df, **mpf_kwargs)
    
    return fig, ax