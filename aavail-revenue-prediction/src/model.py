from pathlib import Path
import joblib, pandas as pd
DEFAULT_MODEL_PATH=Path("artifacts/revenue_model.joblib")
def load_model(path=DEFAULT_MODEL_PATH):
    path=Path(path)
    if not path.exists(): raise FileNotFoundError(f"Trained model not found at {path}. Run src.train first.")
    return joblib.load(path)
def make_prediction(model,target_date,country):
    date=pd.to_datetime(target_date,errors="raise")
    # TODO: replace constant country_code with the same persisted encoder used in training.
    row=pd.DataFrame([{"day_of_week":date.dayofweek,"day_of_month":date.day,"month":date.month,"day_of_year":date.dayofyear,"week_of_year":int(date.isocalendar().week),"country_code":0}])
    return float(model.predict(row)[0])
