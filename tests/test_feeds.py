import os
import pandas as pd
import asyncio
import pytest

from datetime import date

from dumbmoney import get_ohlcv, load_ohlcv_from_csv, export_ohlcv_to_csv
from tests import OUTPUT_DIR


symbols = [
    "ZLAB.US",
    "LABU.US",
    "BRK.A.US",  # US stocks
    "09688.HK",
    "06160.HK",  # HK stocks
    "600745.SH",
    "301308.SZ",
    "603986",
    "002466",  # SH/SZ stocks
    "688235",
    "688472.SH",  # KCB stocks
    "159652.SZ",
    "513090.SH",
    "159792",
    "513040",
    "588080",
    "562500",  # ETF stocks
]


@pytest.mark.asyncio
async def test_get_ohlcv():
    for symbol in symbols:
        df = get_ohlcv(symbol=symbol, fields=[])
        assert not df.empty, f"DataFrame is empty for symbol: {symbol}"
        assert "close" in df.columns, f"'close' column missing for symbol: {symbol}"
        assert df.index.name == "date", f"Index name is not 'date' for symbol: {symbol}"
        assert df.index.is_monotonic_increasing, (
            f"Index is not sorted for symbol: {symbol}"
        )
        assert df.index.dtype == "datetime64[ns]", (
            f"Index is not DatetimeIndex for symbol: {symbol}"
        )
        assert df.index.max() <= pd.Timestamp.now(), (
            f"Index has future dates for symbol: {symbol}"
        )
        print(f"Fetched {len(df)} rows for symbol: {symbol}")
        print(df.tail(3))
        print("...")
        # export to CSV
        csv_path = os.path.join(OUTPUT_DIR, f"{symbol.replace('.', '_')}.csv")
        export_ohlcv_to_csv(df, csv_path)
        # load from CSV
        df_loaded = load_ohlcv_from_csv(csv_path)
        pd.testing.assert_frame_equal(df, df_loaded)
        # rate limit
        print("waiting for 1 second to respect rate limits...")
        await asyncio.sleep(1)


def test_tiger_client():
    try:
        from dumbmoney.feeds.tiger import TigerFeed, TigerConfig
    except ImportError:
        pytest.skip("TigerFeed not available, skipping test.")

    config = TigerConfig(
        private_key=os.getenv("TIGER_PRIVATE_KEY", ""),
        tiger_id=os.getenv("TIGER_ID", ""),
        account=os.getenv("TIGER_ACCOUNT", ""),
        license=os.getenv("TIGER_LICENSE", ""),
    )

    try:
        feed = TigerFeed(config=config)
    except Exception as e:
        pytest.fail(f"Failed to initialize TigerFeed: {e}")

    ohlcv_data = feed.get_ohlcv("002594.SZ", date(2025, 2, 1), date(2026, 1, 25))
    assert not ohlcv_data.empty, "Failed to fetch OHLCV data from TigerFeed."
    print(ohlcv_data.shape)
    print(ohlcv_data.head())
    print("...")
    print(ohlcv_data.tail())
