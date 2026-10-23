import pandas as pd
def aggregate_daily(df):
    required={"date","country","revenue"}; missing=required-set(df.columns)
    if missing: raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    data=df.copy(); data["date"]=pd.to_datetime(data["date"],errors="coerce").dt.floor("D"); data["revenue"]=pd.to_numeric(data["revenue"],errors="coerce")
    data=data.dropna(subset=["date","country","revenue"])
    if data.empty: raise ValueError("No valid transaction rows.")
    by_country=data.groupby(["date","country"],as_index=False)["revenue"].sum().rename(columns={"date":"target_date"})
    combined=data.groupby("date",as_index=False)["revenue"].sum(); combined["country"]="ALL"; combined=combined.rename(columns={"date":"target_date"})
    return pd.concat([by_country,combined],ignore_index=True).sort_values(["country","target_date"]).reset_index(drop=True)
def add_calendar_features(daily):
    out=daily.copy(); dates=pd.to_datetime(out["target_date"])
    out["day_of_week"]=dates.dt.dayofweek; out["day_of_month"]=dates.dt.day; out["month"]=dates.dt.month; out["day_of_year"]=dates.dt.dayofyear; out["week_of_year"]=dates.dt.isocalendar().week.astype(int)
    # Placeholder encoding: persist a country encoder for valid production inference.
    out["country_code"]=out["country"].astype("category").cat.codes
    return out
