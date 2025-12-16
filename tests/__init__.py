import pytest
import os, sys

# Don't write .pyc files
sys.dont_write_bytecode = True

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file if present

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), os.pardir, "outputs")
INPUT_DIR = os.path.join(os.path.dirname(__file__), "ohlcv_data")

# Get sample OHLCV data for testing
from dumbmoney import get_ohlcv, load_ohlcv_from_csv, export_ohlcv_to_csv
@pytest.fixture
def ohlcv_data():
  input_path = os.path.join(INPUT_DIR, "AAPL_US.csv")
  if os.path.isfile(input_path):
    return load_ohlcv_from_csv(input_path)
  else:
    ohlcv = get_ohlcv("AAPL.US", "2024-12-01", "2025-11-30", fields=[])
    export_ohlcv_to_csv(ohlcv, input_path)
    return ohlcv