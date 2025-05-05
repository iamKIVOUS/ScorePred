# backend/ml_model/save_dummy_model.py
import joblib
from ml_model.dummy_model import DummyModel

model = DummyModel()
joblib.dump(model, "model_v1.pkl")
