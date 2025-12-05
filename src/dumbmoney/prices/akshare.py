from datetime import date

import pandas as pd

from .base import BaseProvider, Market, detect_market
from ..types import AdjustType
from ..logger import logger

import akshare as ak


class AkshareProvider(BaseProvider):
  """Data provider using Akshare."""
    
  name = "akshare"
  
  rename_map = {
    "日期": "date",
    "开盘": "open",
    "最高": "high",
    "最低": "low",
    "收盘": "close",
    "成交量": "volume",
  }
  
  adjust_map = {
    "none": "",
    "forward": "qfq",
    "backward": "hfq",
  }

  def supports(self, _: str) -> bool:
    # Akshare supports a wide range of symbols; for simplicity, we assume it supports all.
    return True

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
    
    if market in [Market.SH, Market.SZ]:
      df = ak.stock_zh_a_hist(
        symbol=code,
        period="daily",
        start_date=start_str,
        end_date=end_str,
        adjust=self.adjust_map[adjust],
      )
    elif market == Market.HK:
      df = ak.stock_hk_hist(
        symbol=code,
        period="daily",
        start_date=start_str,
        end_date=end_str,
        adjust=self.adjust_map[adjust],
      )
    elif market == Market.KCB:
      df = ak.stock_zh_kcb_daily(
        symbol=f"sh{code}",
        adjust=self.adjust_map[adjust],
      )
    elif market in [Market.ETF_SH, Market.ETF_SZ]:
      df = ak.fund_etf_hist_em(
        symbol=code,
        start_date=start_str,
        end_date=end_str,
        adjust=self.adjust_map[adjust],
      )
    elif market == Market.US:
      df = ak.stock_us_hist(
        symbol=code,
        period="daily",
        start_date=start_str,
        end_date=end_str,
        adjust=self.adjust_map[adjust],
      )
    else:
      raise ValueError(f"Can't recognize market for symbol: {symbol}")
    
    df = df.rename(columns=self.rename_map)
    df["date"] = pd.to_datetime(df["date"])
    
    # filter df by date range
    df = df[(df["date"] >= pd.to_datetime(start)) & (df["date"] <= pd.to_datetime(end))]
    
    df = df.set_index("date").sort_index()
    
    result = df[["open", "high", "low", "close", "volume"]].copy()
    return pd.DataFrame(result)