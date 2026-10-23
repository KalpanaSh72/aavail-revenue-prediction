import pandas as pd
from src.features import aggregate_daily
def test_aggregate_daily_adds_combined_total():
    df=pd.DataFrame({"date":["2026-01-01","2026-01-01","2026-01-02"],"country":["USA","USA","UK"],"revenue":[10.,5.,7.]})
    out=aggregate_daily(df); all_rows=out[out.country=="ALL"].set_index("target_date")
    assert all_rows.loc[pd.Timestamp("2026-01-01"),"revenue"]==15.
    assert all_rows.loc[pd.Timestamp("2026-01-02"),"revenue"]==7.
