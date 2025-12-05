from dotenv import load_dotenv
load_dotenv()

from dumbmoney import fetch_daily_prices, plot_kline

df = fetch_daily_prices("AAPL.US", start="2025-06-01")
print(df.tail(3))

fig, _ = plot_kline(df, title="AAPL Daily K-Line Chart")

from matplotlib import pyplot as plt
plt.show()

ifig, = plot_kline(df, backend="plotly", title="AAPL Daily K-Line Chart (Plotly)")
ifig.show()
