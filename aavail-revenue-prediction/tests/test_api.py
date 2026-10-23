def test_health_returns_status(client):
    r=client.get("/health"); assert r.status_code==200; assert r.get_json()["status"]=="ok"
def test_predict_rejects_non_json(client):
    r=client.post("/predict",data="not-json",content_type="text/plain"); assert r.status_code==400; assert "error" in r.get_json()
def test_predict_requires_country(client):
    r=client.post("/predict",json={"target_date":"2026-10-01"}); assert r.status_code==400; assert "country" in r.get_json()["error"]
def test_predict_requires_iso_date(client):
    r=client.post("/predict",json={"target_date":"01-10-2026","country":"USA"}); assert r.status_code==400; assert "YYYY-MM-DD" in r.get_json()["error"]
