from typing import Any, Mapping, Optional, List

import pandas as pd

from .base import BaseChart, OHLCData


UP_COLOR = "#26a69a"  # Green for up days
DOWN_COLOR = "#ef5350"  # Red for down days


def infer_offdays_from_index(idx: pd.DatetimeIndex) -> List[pd.Timestamp]:
  """Infer offdays from DatetimeIndex by finding gaps larger than 1 day."""
  dates = idx.normalize().unique()
  all_days = pd.date_range(start=dates.min(), end=dates.max(), freq='D')
  offdays = all_days.difference(dates)
  return list(offdays)


class PlotlyChart(BaseChart):
  """Chart implementation using plotly."""
  
  def __init__(self, default_volume: bool = True, default_height: int = 700):
    super().__init__(default_volume=default_volume)
    self.default_height = default_height
  
  def _plot_kline(
    self,
    ohlc: OHLCData,
    indicators: Optional[Mapping[str, pd.Series]] = None,
    volume: bool = True,
    title: Optional[str] = None,
    height: Optional[int] = None,
    **kwargs
  ) -> Any:
    try:
      import plotly.graph_objects as go
      from plotly.subplots import make_subplots
    except ImportError:
      raise ImportError("plotly is not installed.")
    
    df = ohlc  # type: ignore[assignment]
    idx = df.index
        
    has_volume = volume and "volume" in df.columns
    row_heights = [0.7, 0.3] if has_volume else [1.0]
    rows = 2 if has_volume else 1
    
    fig = make_subplots(
      rows=rows,
      cols=1,
      shared_xaxes=True,
      row_heights=row_heights,
      vertical_spacing=0.03 if has_volume else 0.02,
      subplot_titles=(
        ("Price", "Volume") if has_volume else 
        ("Price",)
      ),
    )
    
    # Candlesticks
    fig.add_trace(
      go.Candlestick(
        x=idx,
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        name="Price",
        **kwargs,
      ),
      row=1,
      col=1,
    )
    
    # Indicators (lines on price panel)
    if indicators:
      for name, series in indicators.items():
        s = series.reindex(idx)
        fig.add_trace(
          go.Scatter(
            x=idx,
            y=s,
            mode="lines",
            name=name,
          ),
          row=1,
          col=1,
        )
        
    # Volume bars in lower panel
    if has_volume:
      up = df["close"] >= df["open"]
      down = ~up
      
      # Volume up
      fig.add_trace(
        go.Bar(
          x=idx[up],
          y=df["volume"][up],
          marker_color=UP_COLOR,
          name="Volume Up",
        ),
        row=2,
        col=1,
      )
      
      # Volume down
      fig.add_trace(
        go.Bar(
          x=idx[down],
          y=df["volume"][down],
          marker_color=DOWN_COLOR,
          name="Volume Down",
        ),
        row=2,
        col=1,
      )
      
    fig.update_layout(
      title_text=title or "Price (K-line) Chart",
      title_x=0.5,
      xaxis_rangeslider_visible=False,
      height=height or self.default_height,
      hovermode="x unified",
      showlegend=False,
      #legend=dict(
      #  orientation="h",
      #  yanchor="bottom",
      #  y=1.02,
      #  xanchor="right",
      #  x=1
      #),
    )
    
    rangebreaks = []
    rangebreaks.append(dict(values=infer_offdays_from_index(idx))) # type: ignore
    if rangebreaks:
      fig.update_xaxes(rangebreaks=rangebreaks)
    
    return fig,