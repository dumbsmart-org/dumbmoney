from typing import List, Literal

from ..models import OHLCVData
from ..indicators import Indicator
from . import adapters # Ensure adapters are registered


PlotterBackend = Literal["mpl", "plotly"]


def plot(
  ohlcv: OHLCVData,
  indicators: List[Indicator],
  title: str = "",
  backend: PlotterBackend = "mpl",
  show: bool = True,
  **kwargs
) -> None:
  """Plot OHLCV data with indicators using the specified backend."""
  
  if backend == "mpl":
    from .mplfinance import MPLFinancePlotter
    plotter = MPLFinancePlotter()
  elif backend == "plotly":
    from .plotly import PlotlyPlotter
    plotter = PlotlyPlotter()
  else:
    raise ValueError(f"Unsupported plotter backend: {backend}")
  
  #series_plots = create_series_plots(indicators)
  
  plotter.plot(
    ohlcv,
    indicators=indicators,
    title=title,
    show=show,
    **kwargs
  )