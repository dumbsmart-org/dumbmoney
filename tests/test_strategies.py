from dumbmoney.strategies import MACrossParams, MACrossStrategy
from dumbmoney.core import SignalType

from tests import ohlcv_data


def test_macross_strategy(ohlcv_data):
  params = MACrossParams(fast_window=5, slow_window=20)
  strategy = MACrossStrategy(params)
  signals = strategy.generate_signals(ohlcv_data)
  assert not signals.signals.empty, "Generated signals DataFrame is empty"
  # Filter LONG signals
  long_signals = signals.signals[signals.signals["signal_type"] == SignalType.LONG]
  assert not long_signals.empty, "No LONG signals generated"
  print(f"Generated {len(long_signals)} LONG signals.")
  print(long_signals)
  flat_signals = signals.signals[(signals.signals["signal_type"] == SignalType.FLAT) & (signals.signals["strength"] > 0.9)]
  assert not flat_signals.empty, "No FLAT signals generated"
  print(f"Generated {len(flat_signals)} FLAT signals.")
  print(flat_signals)