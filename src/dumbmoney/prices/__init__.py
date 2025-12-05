from datetime import date
from functools import lru_cache
from typing import Optional, Any, List

import pandas as pd

from .base import BaseProvider
from .service import PriceService
from ..types import AdjustType


@lru_cache(maxsize=1)
def default_price_service() -> PriceService:
  from .akshare import AkshareProvider
  from .tushare import TushareProvider
  from .massive import MassiveProvider
  
  providers: List[BaseProvider] = [AkshareProvider()]
  
  try:
    tushare_provider = TushareProvider()
    providers.insert(0, tushare_provider)
  except Exception:
    pass
  
  try:
    massive_provider = MassiveProvider()
    providers.insert(0, massive_provider)
  except Exception:
    pass
  
  return PriceService(providers=providers)


def fetch_daily_prices(
  symbol: str,
  start: Optional[Any] = None,
  end: Optional[Any] = None,
  adjust: AdjustType = "forward",
) -> pd.DataFrame:
  end_date: date = end or date.today()
  start_date = start or date(end_date.year - 1, end_date.month, end_date.day)
  service = default_price_service()
  return service.fetch_daily_prices(
    symbol=symbol,
    start=start_date,
    end=end_date,
    adjust=adjust,
  )