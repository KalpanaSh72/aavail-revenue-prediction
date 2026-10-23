import argparse,json
from pathlib import Path
import joblib,numpy as np
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error,mean_squared_error
from src.data_ingestion import load_transactions
from src.features import aggregate_daily,add_calendar_features
FEATURES=["day_of_week","day_of_month","month","day_of_year","week_of_year","country_code"]
def train(data_path,output_dir="artifacts"):
    transactions=load_transactions(data_path); daily=add_calendar_features(aggregate_daily(transactions)).sort_values("target_date").reset_index(drop=True)
    if len(daily)<10: raise ValueError("At least 10 daily/country rows are recommended for a chronological split.")
    split=min(max(1,int(len(daily)*.8)),len(daily)-1); train_df,test_df=daily.iloc[:split],daily.iloc[split:]
    X_train,y_train=train_df[FEATURES],train_df["revenue"]; X_test,y_test=test_df[FEATURES],test_df["revenue"]
    baseline=DummyRegressor(strategy="mean").fit(X_train,y_train); model=RandomForestRegressor(n_estimators=150,random_state=42,min_samples_leaf=2).fit(X_train,y_train)
    def score(estimator):
        pred=estimator.predict(X_test); return {"mae":float(mean_absolute_error(y_test,pred)),"rmse":float(np.sqrt(mean_squared_error(y_test,pred)))}
    result={"baseline":score(baseline),"random_forest":score(model),"test_rows":int(len(test_df)),"feature_columns":FEATURES,"note":"Validate data and feature design before interpreting metrics."}
    output=Path(output_dir); output.mkdir(parents=True,exist_ok=True); joblib.dump(model,output/"revenue_model.joblib"); (output/"metrics.json").write_text(json.dumps(result,indent=2),encoding="utf-8"); return result
if __name__=="__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("--data",default="data/transactions.csv"); parser.add_argument("--output",default="artifacts"); args=parser.parse_args(); print(json.dumps(train(args.data,args.output),indent=2))
