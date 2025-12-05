from abc import ABC, abstractmethod
from typing import Mapping, Optional, Any, Tuple

import pandas as pd


_REQUIRED_COLS = ("open", "high", "low", "close", "volume")


class OHLCData(pd.DataFrame):
  """
  Thin wrapper around pd.DataFrame to represent OHLC data.
  Ensures required columns are present and a DatetimeIndex is used.
  """
  # this is just for type readability - no extra functionality
  pass

    
def _normalize_ohlc(data: pd.DataFrame) -> OHLCData:
  """Ensure DataFrame has required OHLC columns and a DatetimeIndex."""
  df = data.copy()
  df.columns = [col.lower() for col in df.columns]
  
  # Ensure required columns are present
  missing_cols = [col for col in _REQUIRED_COLS if col not in df.columns]
  if missing_cols:
    raise ValueError(f"DataFrame is missing required columns: {missing_cols}")
    
  # Promote 'date' column to index if present
  if not isinstance(df.index, pd.DatetimeIndex):
    for col in df.columns:
      if col.lower() in ("date", "datetime", "trade_date"):
        df[col] = pd.to_datetime(df[col])
        df = df.set_index(col)
        break
    
  if not isinstance(df.index, pd.DatetimeIndex):
    raise ValueError("DataFrame must have a DatetimeIndex or a 'date'/'datetime'/'trade_date' column.")
  
  df = df.sort_index()
  
  # Enforce column order
  cols = [col for col in _REQUIRED_COLS if col in df.columns]
  other_cols = [col for col in df.columns if col not in cols]
  df = df[cols + other_cols]
  
  return df # type: ignore[return-value]
  
  
class BaseChart(ABC):
  """Abstract base class for financial charts."""
  
  def __init__(self, default_volume: bool = True):
    self.default_volume = default_volume
    
  def plot_kline(
    self,
    data: pd.DataFrame,
    indicators: Optional[Mapping[str, pd.Series]] = None,
    volume: Optional[bool] = None,
    title: Optional[str] = None,
    **kwargs
  ) -> Tuple[Any, ...]:
    """Plot OHLC data as a K-line (candlestick) chart."""
    ohlc_data = _normalize_ohlc(data)
    
    if volume is None:
      volume = self.default_volume
      
    return self._plot_kline(
      ohlc_data,
      indicators=indicators,
      volume=bool(volume),
      title=title,
      **kwargs
    )
  
  @abstractmethod
  def _plot_kline(
    self,
    ohlc: OHLCData,
    indicators: Optional[Mapping[str, pd.Series]] = None,
    volume: bool = True,
    title: Optional[str] = None,
    **kwargs
  ) -> Tuple[Any, ...]:
    """Internal method to be implemented by subclasses for plotting."""
    raise NotImplementedError