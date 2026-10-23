from datetime import datetime,timezone
import json,logging,os,time
from pathlib import Path
from flask import Flask,jsonify,request
from src.model import load_model,make_prediction
from src.monitoring import PerformanceMonitor
app=Flask(__name__); LOG_PATH=Path(os.getenv("AAVAIL_LOG_PATH","logs/api.log")); LOG_PATH.parent.mkdir(parents=True,exist_ok=True)
logger=logging.getLogger("aavail_api"); logger.setLevel(logging.INFO)
if not logger.handlers:
    handler=logging.FileHandler(LOG_PATH); handler.setFormatter(logging.Formatter("%(message)s")); logger.addHandler(handler)
monitor=PerformanceMonitor(); MODEL_PATH=os.getenv("AAVAIL_MODEL_PATH","artifacts/revenue_model.joblib")
@app.get("/health")
def health(): return jsonify({"status":"ok","model_available":Path(MODEL_PATH).exists()}),200
@app.get("/metrics")
def metrics(): return jsonify(monitor.summary()),200
@app.post("/predict")
def predict():
    start=time.perf_counter(); ok=False; status=200
    try:
        body=request.get_json(silent=True)
        if not isinstance(body,dict): status=400; return jsonify({"error":"Request body must be a JSON object."}),status
        target_date,country=body.get("target_date"),body.get("country")
        if not isinstance(target_date,str) or not target_date.strip(): status=400; return jsonify({"error":"target_date is required as YYYY-MM-DD."}),status
        try: parsed_date=datetime.strptime(target_date,"%Y-%m-%d").date()
        except ValueError: status=400; return jsonify({"error":"target_date must use YYYY-MM-DD format."}),status
        if not isinstance(country,str) or not country.strip(): status=400; return jsonify({"error":"country is required; use a country name or ALL."}),status
        try: model=load_model(MODEL_PATH)
        except FileNotFoundError: status=503; return jsonify({"error":"Model not trained. Run python -m src.train first."}),status
        prediction=make_prediction(model,parsed_date.isoformat(),country.strip()); ok=True
        return jsonify({"target_date":parsed_date.isoformat(),"country":country.strip(),"predicted_revenue":prediction}),200
    except Exception:
        status=500; app.logger.exception("Prediction failed"); return jsonify({"error":"Prediction failed due to an internal error."}),status
    finally:
        runtime_ms=(time.perf_counter()-start)*1000; monitor.record(runtime_ms,ok=ok); body=request.get_json(silent=True) if request.is_json else {}
        logger.info(json.dumps({"timestamp":datetime.now(timezone.utc).isoformat(),"request_type":"predict","input_data_summary":{"target_date":(body or {}).get("target_date"),"country":(body or {}).get("country")},"runtime_ms":runtime_ms,"success":ok,"status_code":status},default=str))
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.getenv("PORT","5000")),debug=False)
