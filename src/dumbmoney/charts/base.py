from abc import ABC, abstractmethod
from typing import Mapping, Optional, Any, Tuple

import pandas as pd

from ..models import OHLCVData, normalize_ohlcv


UP_COLOR = "#26a69a"  # Green for up days
DOWN_COLOR = "#ef5350"  # Red for down days
  
  
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
    ohlc_data = normalize_ohlcv(data)
    
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
    ohlc: OHLCVData,
    indicators: Optional[Mapping[str, pd.Series]] = None,
    volume: bool = True,
    title: Optional[str] = None,
    **kwargs
  ) -> Tuple[Any, ...]:
    """Internal method to be implemented by subclasses for plotting."""
    raise NotImplementedError