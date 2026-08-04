from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from time import perf_counter
from typing import Any

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.config import (
    FEATURE_COLUMNS,
    FRAUD_THRESHOLD,
    MLFLOW_MODEL_ALIAS,
    MLFLOW_REGISTERED_MODEL_NAME,
)

from src.features.business_features import (
    FEATURE_COLUMNS as BUSINESS_FEATURE_COLUMNS,
    make_business_feature_frame,
    make_business_features,
)

from src.inference.predict import fraud_detection_service

from src.monitoring.metrics import (
    API_ERROR_COUNT,
    API_REQUEST_COUNT,
    API_REQUEST_LATENCY_SECONDS,
    metrics_response,
    record_prediction_metrics,
    update_model_metrics,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

BUSINESS_MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "business_fraud_model.joblib"
)

business_artifact: dict[str, Any] | None = None


def load_business_model() -> dict[str, Any] | None:
    if not BUSINESS_MODEL_PATH.exists():
        return None

    artifact = joblib.load(BUSINESS_MODEL_PATH)

    return artifact


def ensure_fraud_model_loaded() -> bool:
    if fraud_detection_service.is_ready:
        return True

    try:
        fraud_detection_service.load()
        print("Fraud detection model loaded.")

    except Exception as error:
        print(
            "ERROR: Failed to load fraud detection model: "
            f"{error}"
        )

    return fraud_detection_service.is_ready


def ensure_business_model_loaded() -> bool:
    global business_artifact

    if business_artifact is not None:
        return True

    try:
        business_artifact = load_business_model()

        if business_artifact is not None:
            print("Business fraud model loaded.")

    except Exception as error:
        business_artifact = None

        print(
            "ERROR: Failed to load business fraud model: "
            f"{error}"
        )

    return business_artifact is not None


def get_model_version() -> str | None:
    if fraud_detection_service.model_version is not None:
        return str(fraud_detection_service.model_version)

    if fraud_detection_service.is_ready:
        return "local"

    return None


def get_model_source() -> str | None:
    if fraud_detection_service.model_source is not None:
        return str(fraud_detection_service.model_source)

    if fraud_detection_service.is_ready:
        return "local"

    return None


def refresh_monitoring_model_metrics() -> None:
    fraud_model_loaded = ensure_fraud_model_loaded()
    business_model_loaded = ensure_business_model_loaded()

    model_source = get_model_source() or "unknown"
    model_version = get_model_version() or "unknown"

    model_type = (
        type(fraud_detection_service.model).__name__
        if fraud_detection_service.model is not None
        else "unknown"
    )

    update_model_metrics(
        fraud_model_loaded=fraud_model_loaded,
        business_model_loaded=business_model_loaded,
        model_type=model_type,
        model_version=model_version,
        model_source=model_source,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Fraud Detection API...")

    if ensure_fraud_model_loaded():
        print("MLflow/local fraud model loaded.")
    else:
        print("Fraud detection model not loaded.")

    if ensure_business_model_loaded():
        print("Business fraud model loaded.")
    else:
        print(
            "Business fraud model not found. "
            "Run: python -m src.training.train_business_model"
        )

    refresh_monitoring_model_metrics()

    print("Fraud Detection API startup completed.")

    yield

    print("Shutting down Fraud Detection API...")


app = FastAPI(
    title="Real-Time Fraud Detection API",
    description=(
        "Production-oriented machine learning API for real-time "
        "fraud detection using MLflow Model Registry, "
        "business-style feature engineering, and Prometheus monitoring."
    ),
    version="2.1.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def prometheus_metrics_middleware(
    request: Request,
    call_next,
):
    endpoint = request.url.path
    method = request.method

    if endpoint == "/metrics":
        return await call_next(request)

    start_time = perf_counter()
    response = None

    try:
        response = await call_next(request)

        return response

    except Exception:
        API_ERROR_COUNT.labels(
            method=method,
            endpoint=endpoint,
            http_status="500",
        ).inc()

        raise

    finally:
        duration = perf_counter() - start_time

        http_status = (
            str(response.status_code)
            if response is not None
            else "500"
        )

        API_REQUEST_COUNT.labels(
            method=method,
            endpoint=endpoint,
            http_status=http_status,
        ).inc()

        API_REQUEST_LATENCY_SECONDS.labels(
            method=method,
            endpoint=endpoint,
        ).observe(duration)

        if int(http_status) >= 400:
            API_ERROR_COUNT.labels(
                method=method,
                endpoint=endpoint,
                http_status=http_status,
            ).inc()


class TransactionRequest(BaseModel):
    Time: float = Field(
        ...,
        description=(
            "Seconds elapsed between this transaction "
            "and the first transaction."
        ),
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
        ),
    )


class BusinessTransactionRequest(BaseModel):
    amount: float = Field(
        ...,
        ge=0,
        description="Transaction amount.",
    )

    merchant_type: str = Field(
        ...,
        description="Merchant category.",
    )

    location: str = Field(
        ...,
        description="Transaction location.",
    )

    transaction_time: str = Field(
        ...,
        description="Transaction time in HH:MM format.",
    )

    payment_method: str = Field(
        ...,
        description="Payment method.",
    )

    device_type: str = Field(
        ...,
        description="Device type.",
    )

    is_international: bool = Field(
        default=False,
        description="Whether the transaction is international.",
    )

    previous_failed_attempts: int = Field(
        default=0,
        ge=0,
        description="Number of previous failed payment attempts.",
    )


class BusinessPredictionResponse(BaseModel):
    prediction: int
    is_fraud: bool
    fraud_probability: float
    threshold: float
    result: str
    risk_level: str
    model_type: str
    model_version: str
    features_used: int
    engineered_features: dict[str, float]


@app.get(
    "/",
    tags=["Health"],
)
def root():
    return {
        "service": "Real-Time Fraud Detection API",
        "version": "2.1.0",
        "status": "running",
    }


@app.get(
    "/health",
    tags=["Health"],
)
def health_check():
    fraud_model_loaded = ensure_fraud_model_loaded()
    business_model_loaded = ensure_business_model_loaded()

    model_version = get_model_version()
    model_source = get_model_source()

    refresh_monitoring_model_metrics()

    return {
        "status": (
            "healthy"
            if (
                fraud_model_loaded
                or business_model_loaded
            )
            else "unhealthy"
        ),

        "model_loaded": fraud_model_loaded,
        "model_source": model_source,
        "model_version": model_version,

        "mlflow_model": {
            "model_loaded": fraud_model_loaded,
            "model_source": model_source,
            "model_version": model_version,
        },
        "business_model": {
            "model_loaded": business_model_loaded,
            "model_path": str(BUSINESS_MODEL_PATH),
            "model_version": (
                str(
                    business_artifact.get(
                        "model_version",
                        "unknown",
                    )
                )
                if business_artifact is not None
                else None
            ),
        },
        "business_model_loaded": business_model_loaded,
        "message": "Fraud detection API health check completed.",
    }


@app.get(
    "/metrics",
    tags=["Monitoring"],
    include_in_schema=False,
)
def metrics():
    refresh_monitoring_model_metrics()

    return metrics_response()


@app.get(
    "/model-info",
    tags=["Model"],
)
def model_info():
    if not ensure_fraud_model_loaded():
        raise HTTPException(
            status_code=503,
            detail="MLflow champion fraud detection model is not loaded.",
        )

    refresh_monitoring_model_metrics()

    return {
        "registered_model": MLFLOW_REGISTERED_MODEL_NAME,
        "model_alias": f"@{MLFLOW_MODEL_ALIAS}",
        "model_version": get_model_version(),
        "model_type": type(fraud_detection_service.model).__name__,
        "model_source": get_model_source(),
        "features": len(FEATURE_COLUMNS),
        "fraud_threshold": FRAUD_THRESHOLD,
        "status": "loaded",
    }


@app.get(
    "/business-model-info",
    tags=["Model"],
)
def business_model_info():
    if not ensure_business_model_loaded():
        raise HTTPException(
            status_code=503,
            detail=(
                "Business fraud model is not loaded. "
                "Run: python -m src.training.train_business_model"
            ),
        )

    refresh_monitoring_model_metrics()

    return {
        "model_type": business_artifact.get(
            "model_type",
            "Unknown",
        ),
        "model_version": business_artifact.get(
            "model_version",
            "Unknown",
        ),
        "threshold": business_artifact.get(
            "threshold",
            0.5,
        ),
        "features": business_artifact.get(
            "feature_columns",
            BUSINESS_FEATURE_COLUMNS,
        ),
        "metrics": business_artifact.get(
            "metrics",
            {},
        ),
        "status": "loaded",
    }


@app.post(
    "/predict",
    tags=["Prediction"],
)
def predict_transaction(transaction: TransactionRequest):
    if not ensure_fraud_model_loaded():
        raise HTTPException(
            status_code=503,
            detail="MLflow champion fraud detection model is not available.",
        )

    try:
        transaction_data = transaction.model_dump()

        result = fraud_detection_service.predict(
            transaction_data
        )

        prediction_result = str(
            result.get(
                "result",
                "Unknown",
            )
        )

        fraud_probability = float(
            result.get(
                "fraud_probability",
                0.0,
            )
        )

        record_prediction_metrics(
            endpoint="/predict",
            result=prediction_result,
            risk_level="Unknown",
            model_version=get_model_version() or "unknown",
            fraud_probability=fraud_probability,
        )

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=(
                "Prediction failed: "
                f"{str(error)}"
            ),
        )


def classify_risk(probability: float) -> str:
    if probability >= 0.75:
        return "High Risk"

    if probability >= 0.45:
        return "Medium Risk"

    return "Low Risk"


@app.post(
    "/predict-business",
    response_model=BusinessPredictionResponse,
    tags=["Prediction"],
)
def predict_business_transaction(
    transaction: BusinessTransactionRequest,
) -> BusinessPredictionResponse:
    if not ensure_business_model_loaded():
        raise HTTPException(
            status_code=503,
            detail=(
                "Business fraud model is not loaded. "
                "Run: python -m src.training.train_business_model"
            ),
        )

    try:
        model = business_artifact["model"]

        threshold = float(
            business_artifact.get(
                "threshold",
                0.5,
            )
        )

        transaction_data = transaction.model_dump()

        feature_frame = make_business_feature_frame(
            transaction_data
        )

        feature_frame = pd.DataFrame(
            feature_frame,
            columns=BUSINESS_FEATURE_COLUMNS,
        )

        fraud_probability = float(
            model.predict_proba(feature_frame)[0][1]
        )

        prediction = int(
            fraud_probability >= threshold
        )

        engineered_features = make_business_features(
            transaction_data
        )

        result = (
            "Fraud"
            if prediction
            else "Legitimate"
        )

        risk_level = classify_risk(fraud_probability)

        response = BusinessPredictionResponse(
            prediction=prediction,
            is_fraud=bool(prediction),
            fraud_probability=round(
                fraud_probability,
                6,
            ),
            threshold=threshold,
            result=result,
            risk_level=risk_level,
            model_type=str(
                business_artifact.get(
                    "model_type",
                    "Unknown",
                )
            ),
            model_version=str(
                business_artifact.get(
                    "model_version",
                    "Unknown",
                )
            ),
            features_used=len(BUSINESS_FEATURE_COLUMNS),
            engineered_features={
                key: round(
                    float(value),
                    6,
                )
                for key, value in engineered_features.items()
            },
        )

        record_prediction_metrics(
            endpoint="/predict-business",
            result=result,
            risk_level=risk_level,
            model_version=response.model_version,
            fraud_probability=response.fraud_probability,
        )

        return response

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=(
                "Business prediction failed: "
                f"{str(error)}"
            ),
        )
