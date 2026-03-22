import joblib
import os

MODEL_PATH = "model/model.pkl"

def _load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at '{MODEL_PATH}'. "
            "Run 'python train.py' to train and save the model first."
        )
    return joblib.load(MODEL_PATH)

model = _load_model()

def predict_ml_score(features: list) -> float:
    pred = model.predict_proba([features])[0][1]
    return round(pred * 100, 2)