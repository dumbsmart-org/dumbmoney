from datetime import date
from typing import Optional

import os
import pandas as pd

from dumbmoney.providers.base import BaseProvider, Market, detect_market
from dumbmoney.types import AdjustType
from dumbmoney.logger import logger

import tushare as ts


class TushareProvider(BaseProvider):
  """Data provider using Tushare."""
    
  name = "tushare"
  
  rename_map = {
    "trade_date": "date",
    "vol": "volume",
  }
  
  adjust_map = {
    "none": "",
    "forward": "qfq",
    "backward": "hfq",
  }
  
  def __init__(self, api_token: Optional[str] = None) -> None:
    api_token = api_token or os.getenv("TUSHARE_TOKEN")
    if not api_token:
      raise ValueError("TUSHARE_TOKEN environment variable is not set and no api_token provided.")
    ts.set_token(api_token)
    self.pro = ts.pro_api()

  def supports(self, symbol: str) -> bool:
    _, market = detect_market(symbol)
    if market in [Market.SH, Market.SZ, Market.KCB, Market.HK]:
      return True
    return False

  def fetch_daily_prices(
    self,
    symbol: str,
    start: date,
    end: date,
    adjust: AdjustType = "forward",
  ) -> pd.DataFrame:
    start_str = start.strftime("%Y%m%d")
    end_str = end.strftime("%Y%m%d")
    
    code, market = detect_market(symbol)
    logger.debug(f"Fetching {symbol} ({code}) for market {market.name} from {start_str} to {end_str} with adjust={adjust}")
    
    if market in [Market.SH, Market.SZ, Market.KCB]:
      df = ts.pro_bar(
        ts_code=f"{code}.{market.value.split('_')[-1]}",
        adj=self.adjust_map[adjust],
        start_date=start_str,
        end_date=end_str,
      )
    elif market == Market.HK:
      # Only forward adjusted data is supported in Tushare for HK stocks
      df = self.pro.hk_daily_adj(
        ts_code=f"{code}.HK",
        start_date=start_str,
        end_date=end_str,
      )
    else:
      raise ValueError(f"Can't retrieve data for symbol: {symbol}")
    
    df = df.rename(columns=self.rename_map)
    df["date"] = pd.to_datetime(df["date"])
    
    # filter df by date range
    df = df[(df["date"] >= pd.to_datetime(start)) & (df["date"] <= pd.to_datetime(end))]
    
    df = df.set_index("date").sort_index()
    
    result = df[["open", "high", "low", "close", "volume"]].copy()
    return pd.DataFrame(result)