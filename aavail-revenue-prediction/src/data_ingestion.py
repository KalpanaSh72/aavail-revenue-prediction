from pathlib import Path
import os
import pandas as pd
REQUIRED_COLUMNS = {"date", "country", "revenue"}
def load_transactions(path=None):
    path = Path(path or os.getenv("AAVAIL_DATA_PATH", "data/transactions.csv"))
    if not path.exists(): raise FileNotFoundError(f"Dataset not found at {path}. Add the course CSV or set AAVAIL_DATA_PATH.")
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing: raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    df = df.copy(); df["date"] = pd.to_datetime(df["date"], errors="coerce"); df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
    df["country"] = df["country"].astype("string").str.strip(); df = df.dropna(subset=["date", "country", "revenue"])
    if df.empty: raise ValueError("No valid rows remain after parsing required columns.")
    return df.sort_values("date").reset_index(drop=True)
