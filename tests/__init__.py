import pytest
import os
import sys

from dotenv import load_dotenv

# Get sample OHLCV data for testing
from dumbmoney import get_ohlcv, load_ohlcv_from_csv, export_ohlcv_to_csv

# Don't write .pyc files
sys.dont_write_bytecode = True

load_dotenv()  # Load environment variables from .env file if present

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), os.pardir, "outputs")
INPUT_DIR = os.path.join(os.path.dirname(__file__), "ohlcv_data")


@pytest.fixture
def ohlcv_data():
    input_path = os.path.join(INPUT_DIR, "AAPL_US.csv")
    if os.path.isfile(input_path):
        return load_ohlcv_from_csv(input_path)
    else:
        ohlcv = get_ohlcv("AAPL.US", "2024-12-01", "2025-11-30", fields=[])
        export_ohlcv_to_csv(ohlcv, input_path)
        return ohlcv
