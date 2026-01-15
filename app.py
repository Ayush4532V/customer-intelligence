from fastapi import FastAPI
import joblib
import numpy as np
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "models", "random_forest_model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "models", "scaler.pkl"))
feature_columns = joblib.load(os.path.join(BASE_DIR, "models", "feature_columns.pkl"))

app = FastAPI(title="Customer Response Prediction API")
# load model and scaler

@app.get("/")
def home():
    return {"message": "ML Model is running 🚀"}

@app.post("/predict")
def predict(data: dict):
    # Convert input to DataFrame
    input_df = pd.DataFrame([data])

    # Add missing columns with 0
    for col in feature_columns:
        if col not in input_df.columns:
            input_df[col] = 0

    # Reorder columns to match training data
    input_df = input_df[feature_columns]

    # Scale + predict
    input_scaled = scaler.transform(input_df)
    prediction = model.predict(input_scaled)
    probability = model.predict_proba(input_scaled)[0][1]

    return {
        "prediction": int(prediction[0]),
        "probability": round(float(probability), 3)
    }