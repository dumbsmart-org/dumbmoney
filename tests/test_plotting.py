import pytest

from dumbmoney import get_ohlcv, plot
from dumbmoney.indicators import *

from tests import ohlcv_data

@pytest.mark.mpl_image_compare(
  baseline_dir="baseline_images",
  filename="ohlcv_plot.png",
)
def test_plot_ohlcv(ohlcv_data):
  plotter = plot(ohlcv_data, indicators=[], backend="mpl", title="OHLCV Chart")
  return plotter.fig


@pytest.mark.mpl_image_compare(
  baseline_dir="baseline_images",
  filename="ma_plot.png",
)
def test_plot_ma(ohlcv_data):
  ma5 = MovingAverage(window=5, ma_type="SMA")
  ma20 = MovingAverage(window=20, ma_type="SMA")
  ma60 = MovingAverage(window=60, ma_type="SMA")
  ma5.compute(ohlcv_data)
  ma20.compute(ohlcv_data)
  ma60.compute(ohlcv_data)
  plotter = plot(ohlcv_data, indicators=[ma5, ma20, ma60], panels=[0, 0, 0], backend="mpl", title="MA Chart")
  return plotter.fig

@pytest.mark.mpl_image_compare(
  baseline_dir="baseline_images",
  filename="macd_plot.png",
)
def test_plot_macd(ohlcv_data):
  macd = MACD()
  macd.compute(ohlcv_data)
  plotter = plot(ohlcv_data, indicators=[macd], panels=[2], backend="mpl", title="MACD Chart")
  return plotter.fig

@pytest.mark.mpl_image_compare(
  baseline_dir="baseline_images",
  filename="rsi_plot.png",
)
def test_plot_rsi(ohlcv_data):
  rsi = RSI()
  rsi.compute(ohlcv_data)
  plotter = plot(ohlcv_data, indicators=[rsi], panels=[2], backend="mpl", title="RSI Chart")
  return plotter.fig

@pytest.mark.mpl_image_compare(
  baseline_dir="baseline_images",
  filename="combined_plot.png",
)
def test_plot_combined(ohlcv_data):
  ma20 = MovingAverage(window=20, ma_type="SMA")
  macd = MACD()
  rsi = RSI()
  ma20.compute(ohlcv_data)
  macd.compute(ohlcv_data)
  rsi.compute(ohlcv_data)
  plotter = plot(
    ohlcv_data,
    indicators=[ma20, macd, rsi],
    panels=[0, 2, 3],
    backend="mpl",
    title="Combined Chart"
  )
  return plotter.fig