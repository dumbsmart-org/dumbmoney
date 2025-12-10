import pytest
import sys

# Don't write .pyc files
sys.dont_write_bytecode = True

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file if present

# Get sample OHLCV data for testing
from dumbmoney import get_ohlcv
@pytest.fixture
def ohlcv_data():
  return get_ohlcv("AAPL.US", "2025-06-01", "2025-11-30")