from src.model import make_prediction
class DummyModel:
    def predict(self,frame): assert "month" in frame.columns; return [123.45]
def test_make_prediction_returns_float(): assert make_prediction(DummyModel(),"2026-10-01","USA")==123.45
