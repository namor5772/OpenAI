# pip install yfinance pandas
import os, pandas as pd, yfinance as yf
os.environ["YF_NO_CACHE"] = "1"   # avoids cache locks on Windows/OneDrive

tickers = ["BHP.AX", "AMP.AX"]

# ---- Set your desired range here ----
START = "2010-01-01"
END   = None          # or e.g. "2025-10-23"
# -------------------------------------

raw = yf.download(
    tickers,
    start=START, end=END,         # <- use start/end OR period (not both)
    interval="1d",
    group_by="ticker",
    auto_adjust=False,
    threads=False,
    progress=False,
)

def normalize_yf_panel(df, tickers):
    exp = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
    if not isinstance(df.columns, pd.MultiIndex):
        df = pd.concat({tickers[0]: df}, axis=1)

    level0 = set(df.columns.get_level_values(0))
    if set(exp).issubset(level0):
        tidy = (
            df.stack(level=1, future_stack=True)
              .rename_axis(index=["date", "ticker"])
              .reset_index()
        )
    else:
        tidy = (
            df.swaplevel(axis=1)
              .stack(level=1, future_stack=True)
              .rename_axis(index=["date", "ticker"])
              .reset_index()
        )

    tidy = tidy.rename(columns={
        "Open": "open", "High": "high", "Low": "low",
        "Close": "close", "Adj Close": "adj_close", "Volume": "volume",
    })
    keep = ["date", "ticker", "open", "high", "low", "close", "adj_close", "volume"]
    tidy = tidy[[c for c in keep if c in tidy.columns]]
    return tidy

tidy = normalize_yf_panel(raw, tickers)
tidy["date"] = pd.to_datetime(tidy["date"])

# --- Verify what you actually got ---
by_ticker = tidy.groupby("ticker")["date"]
summary = pd.DataFrame({
    "first_date": by_ticker.min(),
    "last_date":  by_ticker.max(),
    "rows":       tidy.groupby("ticker").size()
})
print("Download summary by ticker:")
print(summary.to_string())

# --- Print a small sample WITHOUT truncating to 3 days only ---
print("\nSample rows (head 2 + tail 2 per ticker):")
sample = (
    tidy.sort_values(["ticker", "date"])
        .groupby("ticker", group_keys=True)
        .apply(lambda d: pd.concat([d.head(2), d.tail(2)]))
        .reset_index(level=0, drop=True)
)
print(sample.to_string(index=False))

# --- Optional sanity checks (remove if you don't want assertions) ---
assert (summary["rows"] > 3).all(), "Looks like you only fetched a few days. Check for an accidental 'period=' in yf.download."
if END:
    assert (summary["last_date"] <= pd.to_datetime(END)).all(), "Pulled beyond END; adjust filtering if needed."
assert (summary["first_date"] <= pd.to_datetime(START)).all(), "Did not reach requested START; try an earlier START or different source."
