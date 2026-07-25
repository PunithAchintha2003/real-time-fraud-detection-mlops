from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# PROJECT CONFIGURATION

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "fraud_detection_model.joblib"
)

SCALER_PATH = (
    BASE_DIR
    / "models"
    / "scaler.joblib"
)


# FASTAPI APPLICATION

app = FastAPI(
    title="Real-Time Fraud Detection API",
    description=(
        "Machine Learning API for credit card "
        "fraud detection using Random Forest."
    ),
    version="1.0.0",
)

# LOAD MODEL AND SCALER

try:

    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    print("Model loaded successfully.")
    print(f"Model path: {MODEL_PATH}")

    print("Scaler loaded successfully.")
    print(f"Scaler path: {SCALER_PATH}")

except Exception as error:

    print(
        f"Failed to load model or scaler: {error}"
    )

    model = None
    scaler = None

# REQUEST SCHEMA

class TransactionRequest(BaseModel):
    """
    Request schema for a credit card transaction.

    The dataset contains 30 input features:
    Time, V1-V28, and Amount.
    """

    Time: float = Field(
        ...,
        description="Seconds elapsed between this transaction and the first transaction."
    )

    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float

    Amount: float = Field(
        ...,
        ge=0,
        description="Transaction amount."
    )

# HEALTH CHECK ENDPOINT

@app.get("/health")
def health_check():
    """
    Check whether the API and ML model are ready.
    """

    if model is None or scaler is None:

        return {
            "status": "unhealthy",
            "model_loaded": False,
            "message": "Model or scaler failed to load."
        }

    return {
        "status": "healthy",
        "model_loaded": True,
        "message": "Fraud detection API is ready."
    }

# MODEL INFORMATION ENDPOINT

@app.get("/model-info")
def model_info():
    """
    Return information about the currently loaded model.
    """

    if model is None:

        raise HTTPException(
            status_code=503,
            detail="Model is not loaded."
        )

    return {
        "model_type": type(model).__name__,
        "model_path": str(MODEL_PATH),
        "scaler_path": str(SCALER_PATH),
        "features": 30,
        "status": "loaded"
    }

# PREDICTION ENDPOINT

@app.post("/predict")
def predict_transaction(
    transaction: TransactionRequest
):
    """
    Predict whether a credit card transaction is fraudulent.
    """

    if model is None or scaler is None:

        raise HTTPException(
            status_code=503,
            detail="Model or scaler is not available."
        )

    try:

        # Convert request data into dictionary
        transaction_data = transaction.model_dump()

        # Convert dictionary into DataFrame
        input_data = pd.DataFrame(
            [transaction_data]
        )

        # Scale Time and Amount
        input_data[["Time", "Amount"]] = (
            scaler.transform(
                input_data[["Time", "Amount"]]
            )
        )

        # Generate prediction
        prediction = model.predict(
            input_data
        )[0]

        # Generate fraud probability
        fraud_probability = model.predict_proba(
            input_data
        )[0][1]

        # Convert prediction to integer
        prediction = int(prediction)

        # Convert probability to float
        fraud_probability = float(
            fraud_probability
        )

        # Return prediction response
        return {
            "prediction": prediction,
            "is_fraud": bool(prediction == 1),
            "fraud_probability": round(
                fraud_probability,
                4
            ),
            "result": (
                "Fraudulent"
                if prediction == 1
                else "Legitimate"
            )
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(error)}"
        )