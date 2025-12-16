from dotenv import load_dotenv
load_dotenv()

from dumbmoney import get_ohlcv, plot

ohlcv = get_ohlcv("HSAI.US", fields=[])
print(ohlcv.tail(5))

from dumbmoney.indicators import MovingAverage, MACD, RSI

ma20 = MovingAverage(name="MA20", window=20, ma_type="SMA")
ma20.compute(ohlcv)
print(ma20.values.tail(5))

ma5 = MovingAverage(name="MA5", window=5, ma_type="SMA")
ma5.compute(ohlcv)

ma60 = MovingAverage(name="MA60", window=60, ma_type="SMA")
ma60.compute(ohlcv)

vol_ma20 = MovingAverage(name="Vol_MA20", window=20, ma_type="SMA", input_col="volume")
vol_ma20.compute(ohlcv)
print(vol_ma20.values.tail(5))

macd = MACD()
macd.compute(ohlcv)
print(macd.values.tail(5))

rsi = RSI()
rsi.compute(ohlcv)
print(rsi.values.tail(5))

#plot(
#  ohlcv,
#  indicators=[ma5, ma20, ma60, vol_ma20, macd, rsi],
#  panels=[0, 0, 0, 1, 2, 3],
#  title="AAPL Stock Price with Indicators (mplfinance)",
#  backend="mpl", # available backends: "mpl", "plotly"
#)

plot(
  ohlcv,
  indicators=[ma5, ma20, ma60, vol_ma20, macd, rsi],
  panels=[0, 0, 0, 1, 2, 3],
  title="AAPL Stock Price with Indicators (Plotly)",
  backend="plotly"
)