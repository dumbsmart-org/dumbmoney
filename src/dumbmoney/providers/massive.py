from dataclasses import asdict
from datetime import date, datetime
from typing import Optional

import os
import pandas as pd

from dumbmoney.providers.base import BaseProvider, Market, detect_market
from dumbmoney.types import AdjustType
from dumbmoney.logger import logger

from massive import RESTClient


class MassiveProvider(BaseProvider):
  """Data provider using Massive."""
    
  name = "massive"
  
  def __init__(self, api_key: Optional[str] = None) -> None:
    api_key = api_key or os.getenv("MASSIVE_KEY")
    if not api_key:
      raise ValueError("MASSIVE_KEY environment variable is not set and no api_key provided.")
    self.client = RESTClient(api_key)

  def supports(self, symbol: str) -> bool:
    _, market = detect_market(symbol)
    if market in [Market.US]:
      return True
    return False

  def fetch_daily_prices(
    self,
    symbol: str,
    start: date,
    end: date,
    adjust: AdjustType = "forward",
  ) -> pd.DataFrame:
    start_str = start.strftime("%Y-%m-%d")
    end_str = end.strftime("%Y-%m-%d")
    
    code, market = detect_market(symbol)
    logger.debug(f"Fetching {symbol} ({code}) for market {market.name} from {start_str} to {end_str} with adjust={adjust}")
    
    if market in [Market.US]:
      aggs = []
      for a in self.client.list_aggs(
        code,
        1,
        "day",
        start_str,
        end_str,
        adjusted=(adjust != "none"),
      ):
        aggs.append(a)
        
      df = pd.DataFrame([asdict(a) for a in aggs])
    else:
      raise ValueError(f"Can't retrieve data for symbol: {symbol}")
    
    df["date"] = pd.to_datetime(df["timestamp"].apply(lambda ts: datetime.fromtimestamp(ts / 1000).date()))
    
    # filter df by date range
    df = df[(df["date"] >= pd.to_datetime(start)) & (df["date"] <= pd.to_datetime(end))]
    
    df = df.set_index("date").sort_index()
    
    result = df[["open", "high", "low", "close", "volume"]].copy()
    return pd.DataFrame(result)