from abc import ABC, abstractmethod
from datetime import date
from enum import Enum
from typing import Tuple

import pandas as pd
import re

from ..types import AdjustType


class Market(str, Enum):
  SZ = "SZ"
  SH = "SH"
  HK = "HK"
  KCB = "KCB_SH"
  ETF_SZ = "ETF_SZ"
  ETF_SH = "ETF_SH"
  US = "US"
  UNKNOWN = "UNKNOWN"


def detect_market(symbol: str) -> Tuple[str, Market]:
  """
  Helper function to detect market from symbol.
  
  Args:
    symbol: str, e.g. "000001.SZ", "AAPL.US", "06966.HK", etc. Suffixes are not required for CN_A/CN_KCB/CN_ETF shares. However, if present, they must be valid.
    
  Returns:
    Tuple[str, Market]: A tuple containing the code and the Market enum value.
  """
  symbol = symbol.strip().upper()
  
  if "." in symbol:
    code, suffix = symbol.rsplit(".", 1)
  else:
    code = symbol
    suffix = ""
    
  if suffix == "US" and len(code) <= 5:
    return code, Market.US
  
  if re.match(r"^\d{4,5}$", code) and suffix == "HK":
    return code, Market.HK
  
  if re.match(r"^60\d{4}$", code) and suffix in ["SH", ""]:
    return code, Market.SH
  
  if re.match(r"^(00|30)\d{4}$", code) and suffix in ["SZ", ""]:
    return code, Market.SZ
  
  if re.match(r"^68\d{4}$", code) and suffix in ["SH", ""]:
    return code, Market.KCB
  
  if re.match(r"^5[168]\d{4}$", code) and suffix in ["SH", ""]:
    return code, Market.ETF_SH
  
  if re.match(r"^15\d{4}$", code) and suffix in ["SZ", ""]:
    return code, Market.ETF_SZ
  
  return code, Market.UNKNOWN


class BaseProvider(ABC):
  """Interface for data providers."""
  
  name: str
  
  @abstractmethod
  def supports(self, symbol: str) -> bool:
    """Return True if the provider can handle the given symbol."""
    raise NotImplementedError
  
  @abstractmethod
  def fetch_daily_prices(
    self,
    symbol: str,
    start: date,
    end: date,
    adjust: AdjustType = "forward",
  ) -> pd.DataFrame:
    """
    Fetch daily price data for the given symbol and date range.
    
    Return a DataFrame with:
    - index: DatetimeIndex named 'date'
    - columns: ['open', 'high', 'low', 'close', 'volume']
    """
    raise NotImplementedError