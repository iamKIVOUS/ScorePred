# backend/ml_model/dummy_model.py
import numpy as np

class DummyModel:
    def predict(self, X):
        return [0 if x[0] > 0.5 else 1 for x in X]

    def predict_proba(self, X):
        return [[0.8, 0.2] if x[0] > 0.5 else [0.3, 0.7] for x in X]
