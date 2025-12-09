import pytest

from dumbmoney import get_ohlcv
from dumbmoney.indicators import MovingAverage, MACD, RSI

# Get sample OHLCV data for testing
@pytest.fixture
def ohlcv_data():
  return get_ohlcv("AAPL.US", "2025-01-01", "2025-06-30")

def test_moving_average(ohlcv_data):
  window = 20
  ma20 = MovingAverage(window=window, ma_type="SMA")
  values = ma20.compute(ohlcv_data)
  assert len(values.columns) == 1  # Single output
  assert len(values) == len(ohlcv_data)
  assert values.iloc[:, 0].isnull().sum() == window - 1  # First (window - 1) values should be NaN
    
def test_macd(ohlcv_data):
  macd = MACD()
  values = macd.compute(ohlcv_data)
  assert len(values.columns) == 3  # macd, signal, histogram
  assert len(values) == len(ohlcv_data)
    
    
def test_rsi(ohlcv_data):
  window = 14
  rsi = RSI(window=window)
  values = rsi.compute(ohlcv_data)
  assert len(values) == len(ohlcv_data)
  assert len(values.columns) == 1
  assert values.iloc[:, 0].isnull().sum() == window  # First 14 values should be NaN