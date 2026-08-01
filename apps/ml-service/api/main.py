from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.config import (
    FRAUD_THRESHOLD,
    MLFLOW_MODEL_ALIAS,
    MLFLOW_REGISTERED_MODEL_NAME,
    FEATURE_COLUMNS,
)

from src.inference.predict import (
    fraud_detection_service,
)


# APPLICATION LIFESPAN

@asynccontextmanager
async def lifespan(app: FastAPI):

    print(
        "Starting Fraud Detection API..."
    )

    try:

        fraud_detection_service.load()

        print(
            "Fraud Detection API startup completed."
        )

    except Exception as error:

        print(
            "ERROR: Failed to load "
            f"fraud detection model: {error}"
        )

        # Keep API running.
        # /health reports unhealthy.
        # /predict and /model-info return 503.

    yield

    print(
        "Shutting down Fraud Detection API..."
    )


# FASTAPI APPLICATION

app = FastAPI(

    title="Real-Time Fraud Detection API",

    description=(
        "Production-oriented machine learning API "
        "for real-time credit card fraud detection "
        "using MLflow Model Registry."
    ),

    version="1.0.0",

    lifespan=lifespan,
)


# REQUEST SCHEMA

class TransactionRequest(BaseModel):
    """
    Request schema for credit card transaction.

    The trained model expects exactly 30 features:

    - Time
    - V1 to V28
    - Amount
    """

    Time: float = Field(
        ...,
        description=(
            "Seconds elapsed between this transaction "
            "and the first transaction."
        )
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
        description=(
            "Credit card transaction amount. "
            "Must be greater than or equal to 0."
        )
    )


# ROOT ENDPOINT

@app.get(
    "/",
    tags=["Health"]
)
def root():

    return {
        "service": "Real-Time Fraud Detection API",
        "version": "1.0.0",
        "status": "running"
    }


# HEALTH CHECK

@app.get(
    "/health",
    tags=["Health"]
)
def health_check():

    if not fraud_detection_service.is_ready:

        return {

            "status": "unhealthy",

            "model_loaded": False,

            "model_source": (
                fraud_detection_service.model_source
            ),

            "model_version": (
                str(
                    fraud_detection_service.model_version
                )
                if fraud_detection_service.model_version
                is not None
                else None
            ),

            "message": (
                "Model or scaler is not available."
            )
        }

    return {

        "status": "healthy",

        "model_loaded": True,

        "model_source": (
            fraud_detection_service.model_source
        ),

        "model_version": (
            str(
                fraud_detection_service.model_version
            )
            if fraud_detection_service.model_version
            is not None
            else None
        ),

        "message": (
            "Fraud detection API is ready."
        )
    }


# MODEL INFORMATION

@app.get(
    "/model-info",
    tags=["Model"]
)
def model_info():

    if not fraud_detection_service.is_ready:

        raise HTTPException(

            status_code=503,

            detail=(
                "Model is not loaded."
            )
        )

    return {

        "registered_model": (
            MLFLOW_REGISTERED_MODEL_NAME
        ),

        "model_alias": (
            f"@{MLFLOW_MODEL_ALIAS}"
        ),

        "model_version": (
            str(
                fraud_detection_service.model_version
            )
            if fraud_detection_service.model_version
            is not None
            else None
        ),

        "model_type": (
            type(
                fraud_detection_service.model
            ).__name__
        ),

        "model_source": (
            fraud_detection_service.model_source
        ),

        "features": len(
            FEATURE_COLUMNS
        ),

        "fraud_threshold": (
            FRAUD_THRESHOLD
        ),

        "status": "loaded"
    }


# PREDICTION ENDPOINT

@app.post(
    "/predict",
    tags=["Prediction"]
)
def predict_transaction(
    transaction: TransactionRequest
):

    # CHECK MODEL AVAILABILITY

    if not fraud_detection_service.is_ready:

        raise HTTPException(

            status_code=503,

            detail=(
                "Fraud detection model is not available."
            )
        )

    try:

        # Convert Pydantic model to dictionary
        transaction_data = (
            transaction.model_dump()
        )

        # Generate prediction
        result = (
            fraud_detection_service.predict(
                transaction_data
            )
        )

        return result

    except ValueError as error:

        raise HTTPException(

            status_code=400,

            detail=str(
                error
            )
        )

    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=(
                "Prediction failed: "
                f"{str(error)}"
            )
        )