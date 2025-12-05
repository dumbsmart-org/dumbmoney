import pytest

from dumbmoney import fetch_daily_prices, plot_kline

@pytest.mark.mpl_image_compare(
  baseline_dir="baseline_images",
  filename="aapl_kline_chart.png"
)
def test_plot_kline():
  data = fetch_daily_prices("AAPL.US", start="2025-06-01", end="2025-11-30")
  fig, _ = plot_kline(data, title="AAPL Daily K-Line Chart")
  return fig