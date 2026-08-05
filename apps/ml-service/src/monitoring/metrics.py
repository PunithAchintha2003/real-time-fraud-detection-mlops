from __future__ import annotations

from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)
from starlette.responses import Response


API_REQUEST_COUNT = Counter(
    "fraud_api_requests_total",
    "Total number of HTTP requests received by the Fraud Detection API.",
    [
        "method",
        "endpoint",
        "http_status",
    ],
)

API_REQUEST_LATENCY_SECONDS = Histogram(
    "fraud_api_request_duration_seconds",
    "HTTP request latency in seconds for the Fraud Detection API.",
    [
        "method",
        "endpoint",
    ],
)

API_ERROR_COUNT = Counter(
    "fraud_api_errors_total",
    "Total number of HTTP error responses from the Fraud Detection API.",
    [
        "method",
        "endpoint",
        "http_status",
    ],
)

FRAUD_MODEL_LOADED = Gauge(
    "fraud_model_loaded",
    "Whether the MLflow/local fraud detection model is loaded. 1 means loaded, 0 means not loaded.",
)

BUSINESS_MODEL_LOADED = Gauge(
    "business_fraud_model_loaded",
    "Whether the business fraud detection model is loaded. 1 means loaded, 0 means not loaded.",
)

MODEL_INFO = Gauge(
    "fraud_model_info",
    "Information about the loaded fraud detection model.",
    [
        "model_type",
        "model_version",
        "model_source",
    ],
)

PREDICTION_COUNT = Counter(
    "fraud_predictions_total",
    "Total number of fraud predictions made by the API.",
    [
        "endpoint",
        "result",
        "risk_level",
        "model_version",
    ],
)

FRAUD_PREDICTION_COUNT = Counter(
    "fraud_predictions_fraud_total",
    "Total number of predictions classified as fraud.",
    [
        "endpoint",
        "model_version",
    ],
)

LEGITIMATE_PREDICTION_COUNT = Counter(
    "fraud_predictions_legitimate_total",
    "Total number of predictions classified as legitimate.",
    [
        "endpoint",
        "model_version",
    ],
)

PREDICTION_PROBABILITY = Histogram(
    "fraud_prediction_probability",
    "Distribution of fraud prediction probabilities.",
    [
        "endpoint",
        "result",
        "risk_level",
    ],
    buckets=[
        0.0,
        0.1,
        0.2,
        0.3,
        0.4,
        0.5,
        0.6,
        0.7,
        0.8,
        0.9,
        1.0,
    ],
)


def update_model_metrics(
    fraud_model_loaded: bool,
    business_model_loaded: bool,
    model_type: str,
    model_version: str,
    model_source: str,
) -> None:
    FRAUD_MODEL_LOADED.set(
        1
        if fraud_model_loaded
        else 0
    )

    BUSINESS_MODEL_LOADED.set(
        1
        if business_model_loaded
        else 0
    )

    MODEL_INFO.labels(
        model_type=model_type,
        model_version=model_version,
        model_source=model_source,
    ).set(1)


def record_prediction_metrics(
    endpoint: str,
    result: str,
    risk_level: str,
    model_version: str,
    fraud_probability: float,
) -> None:
    normalized_result = result.lower()

    PREDICTION_COUNT.labels(
        endpoint=endpoint,
        result=result,
        risk_level=risk_level,
        model_version=model_version,
    ).inc()

    PREDICTION_PROBABILITY.labels(
        endpoint=endpoint,
        result=result,
        risk_level=risk_level,
    ).observe(fraud_probability)

    if normalized_result == "fraud":
        FRAUD_PREDICTION_COUNT.labels(
            endpoint=endpoint,
            model_version=model_version,
        ).inc()

    else:
        LEGITIMATE_PREDICTION_COUNT.labels(
            endpoint=endpoint,
            model_version=model_version,
        ).inc()


def metrics_response() -> Response:
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
