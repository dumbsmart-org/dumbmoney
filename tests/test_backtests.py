from dumbmoney.strategies import MACrossParams, MACrossStrategy
from dumbmoney.policies import LongFlatAllInConfig, LongFlatAllInPolicy
from dumbmoney.backtests.single_asset import SingleAssetBacktester

from tests import ohlcv_data


def test_SingleAsset_MACrossStrategy_LongFlatAllInPolicy(ohlcv_data):
  strategy = MACrossStrategy(MACrossParams(fast_window=5, slow_window=20))
  policy = LongFlatAllInPolicy(LongFlatAllInConfig(max_long_pct=1.0, min_strength=0.5))
  backtester = SingleAssetBacktester(initial_cash=100_000.0)
  result = backtester.run(symbol="AAPL", ohlcv=ohlcv_data, strategy=strategy, policy=policy)
  assert len(result.trades) == 17, f"Expected 17 trades, got {len(result.trades)}"
  assert abs(result.metrics.total_return - -0.109) < 1e-3, f"Expected total return approx -10.9%, got {result.metrics.total_return}"
  assert abs(result.metrics.max_drawdown - -0.222) < 1e-3, f"Expected max drawdown approx -22.2%, got {result.metrics.max_drawdown}"
  assert result.metrics.sharpe_ratio is not None and abs(result.metrics.sharpe_ratio - -0.575) < 1e-3, f"Expected sharpe ratio approx -0.575, got {result.metrics.sharpe_ratio}"
  
  strategy = MACrossStrategy(MACrossParams(fast_window=20, slow_window=60))
  result = backtester.run(symbol="AAPL", ohlcv=ohlcv_data, strategy=strategy, policy=policy)
  print(f"Trades executed: {len(result.trades)}")
  print(f"metrics: {result.metrics}")
  assert len(result.trades) == 1, f"Expected 1 trade, got {len(result.trades)}"
  
  