from datetime import date, datetime
from typing import List, Sequence

import pandas as pd

from .base import BaseProvider
from ..types import AdjustType


def _normalize_date(d) -> date:
  if isinstance(d, datetime):
    return d.date()
  if isinstance(d, date):
    return d
  if isinstance(d, str):
    return datetime.fromisoformat(d).date()
  raise ValueError(f"Invalid date type: {type(d)}")


class PriceService:
  """Service to fetch price data using multiple providers (potentially)."""
  
  def __init__(self, providers: Sequence[BaseProvider]) -> None:
    if not providers:
      raise ValueError("At least one provider must be provided.")
    self.providers = list(providers)
    
  def _pick_providers(self, symbol: str) -> List[BaseProvider]:
    candidates = [p for p in self.providers if p.supports(symbol)]
    if not candidates:
      raise ValueError(f"No provider found for symbol: {symbol}")
    return candidates
  
  def fetch_daily_prices(
    self,
    symbol: str,
    start,
    end,
    adjust: AdjustType = "forward",
  ) -> pd.DataFrame:
    start_date = _normalize_date(start)
    end_date = _normalize_date(end)
    
    errors: List[str] = []
    
    for provider in self._pick_providers(symbol):
      try:
        df = provider.fetch_daily_prices(
          symbol=symbol,
          start=start_date,
          end=end_date,
          adjust=adjust,
        )
        return df
      except Exception as e:
        errors.append(f"Provider {provider.name} failed: {e}")

    raise RuntimeError(
      f"All providers failed for symbol: {symbol} "
      f"({start_date} → {end_date}): {'; '.join(errors)}"
    )