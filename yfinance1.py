# pip install yfinance pandas
import os, pandas as pd, yfinance as yf
os.environ["YF_NO_CACHE"] = "1"   # avoids Windows/OneDrive cache locks

tickers = ["BHP.AX", "AMP.AX"]
raw = yf.download(
    tickers,
    period="1mo", interval="1d",
    group_by="ticker",
    auto_adjust=False,
    threads=False,      # important on Windows to avoid cache lock
    progress=False
)

def normalize_yf_panel(df, tickers):
    """
    Convert the wide yfinance panel (MultiIndex columns) into a tidy long DataFrame:
    columns -> date, ticker, open, high, low, close, adj_close, volume
    Works regardless of whether level 0 or level 1 is ticker.
    """
    # Standard OHLCV names we expect from yfinance
    exp = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]

    if not isinstance(df.columns, pd.MultiIndex):
        # Single-ticker case: add ticker level, then fall through
        df = pd.concat({tickers[0]: df}, axis=1)

    # Figure out which level is the ticker
    level0 = set(df.columns.get_level_values(0))
    level1 = set(df.columns.get_level_values(1))

    if set(exp).issubset(level0):
        # Level 0 = fields, Level 1 = tickers
        tidy = (
            df.stack(level=1)                 # index: date, ticker
              .rename_axis(index=["date", "ticker"])
              .reset_index()
        )
    else:
        # Level 0 = tickers, Level 1 = fields
        tidy = (
            df.swaplevel(axis=1)              # make level 0 = fields
              .stack(level=1)
              .rename_axis(index=["date", "ticker"])
              .reset_index()
        )

    # Standardize column names
    tidy = tidy.rename(
        columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Adj Close": "adj_close",
            "Volume": "volume"
        }
    )

    # Keep only the expected columns (some feeds include others)
    keep = ["date", "ticker", "open", "high", "low", "close", "adj_close", "volume"]
    tidy = tidy[[c for c in keep if c in tidy.columns]]

    # Sort for nice display
    tidy = tidy.sort_values(["ticker", "date"]).reset_index(drop=True)
    return tidy

tidy = normalize_yf_panel(raw, tickers)

# Show last 3 rows per ticker
print(
    tidy.groupby("ticker", group_keys=False)
        .apply(lambda d: d.tail(3))
        .to_string(index=False)
)
