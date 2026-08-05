from __future__ import annotations

from collections import defaultdict, deque
from typing import Deque

from prometheus_client import Counter, Gauge, Histogram


ML_MONITORED_FEATURES = [
    "amount",
    "log_amount",
    "hour",
    "is_night_transaction",
    "merchant_risk_score",
    "location_risk_score",
    "payment_method_risk",
    "device_risk_score",
    "is_international",
    "previous_failed_attempts",
    "failed_attempt_risk",
    "amount_risk_score",
    "total_business_risk_score",
]


ML_FEATURE_BASELINE_STATS = {
    "amount": {
        "mean": 3500.0,
        "std": 3000.0,
    },
    "log_amount": {
        "mean": 7.5,
        "std": 1.5,
    },
    "hour": {
        "mean": 13.0,
        "std": 6.0,
    },
    "is_night_transaction": {
        "mean": 0.25,
        "std": 0.43,
    },
    "merchant_risk_score": {
        "mean": 0.45,
        "std": 0.25,
    },
    "location_risk_score": {
        "mean": 0.35,
        "std": 0.25,
    },
    "payment_method_risk": {
        "mean": 0.35,
        "std": 0.25,
    },
    "device_risk_score": {
        "mean": 0.30,
        "std": 0.25,
    },
    "is_international": {
        "mean": 0.20,
        "std": 0.40,
    },
    "previous_failed_attempts": {
        "mean": 1.0,
        "std": 1.5,
    },
    "failed_attempt_risk": {
        "mean": 0.30,
        "std": 0.30,
    },
    "amount_risk_score": {
        "mean": 0.35,
        "std": 0.30,
    },
    "total_business_risk_score": {
        "mean": 0.40,
        "std": 0.25,
    },
}


ML_MONITORING_WINDOW_SIZE = 50
ML_DRIFT_WARNING_THRESHOLD = 2.0
ML_DRIFT_CRITICAL_THRESHOLD = 3.0


feature_windows: dict[str, Deque[float]] = defaultdict(
    lambda: deque(maxlen=ML_MONITORING_WINDOW_SIZE)
)

prediction_totals = {
    "total": 0,
    "fraud": 0,
    "legitimate": 0,
}


ML_BUSINESS_PREDICTIONS_TOTAL = Counter(
    "ml_business_predictions_total",
    "Total number of business fraud predictions monitored.",
    [
        "result",
        "risk_level",
        "model_version",
    ],
)

ML_BUSINESS_FRAUD_RATE = Gauge(
    "ml_business_fraud_rate",
    "Current fraud prediction rate from monitored business predictions.",
)

ML_BUSINESS_LEGITIMATE_RATE = Gauge(
    "ml_business_legitimate_rate",
    "Current legitimate prediction rate from monitored business predictions.",
)

ML_BUSINESS_PREDICTION_WINDOW_SIZE = Gauge(
    "ml_business_prediction_window_size",
    "Number of predictions used in the current ML monitoring window.",
)

ML_BUSINESS_AMOUNT_DISTRIBUTION = Histogram(
    "ml_business_amount_distribution",
    "Distribution of monitored business transaction amounts.",
    buckets=[
        0,
        100,
        500,
        1000,
        2500,
        5000,
        7500,
        10000,
        25000,
        50000,
        100000,
    ],
)

ML_BUSINESS_PROBABILITY_DISTRIBUTION = Histogram(
    "ml_business_probability_distribution",
    "Distribution of business fraud prediction probabilities.",
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

ML_BUSINESS_RISK_SCORE_DISTRIBUTION = Histogram(
    "ml_business_total_risk_score_distribution",
    "Distribution of engineered total business risk scores.",
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

ML_BUSINESS_FEATURE_VALUE = Histogram(
    "ml_business_feature_value",
    "Distribution of monitored business feature values.",
    [
        "feature_name",
    ],
    buckets=[
        0,
        0.1,
        0.2,
        0.3,
        0.4,
        0.5,
        0.6,
        0.7,
        0.8,
        0.9,
        1,
        2,
        5,
        10,
        25,
        50,
        100,
        500,
        1000,
        5000,
        10000,
        50000,
        100000,
    ],
)

ML_BUSINESS_FEATURE_DRIFT_SCORE = Gauge(
    "ml_business_feature_drift_score",
    "Simple drift score comparing rolling feature mean against baseline mean.",
    [
        "feature_name",
    ],
)

ML_BUSINESS_DRIFT_ALERTS_TOTAL = Counter(
    "ml_business_drift_alerts_total",
    "Total number of simple drift alerts detected for monitored business features.",
    [
        "feature_name",
        "severity",
    ],
)


def calculate_rolling_mean(values: Deque[float]) -> float:
    if not values:
        return 0.0

    return sum(values) / len(values)


def calculate_feature_drift_score(
    feature_name: str,
    rolling_mean: float,
) -> float:
    baseline = ML_FEATURE_BASELINE_STATS.get(feature_name)

    if baseline is None:
        return 0.0

    baseline_mean = float(
        baseline["mean"]
    )

    baseline_std = float(
        baseline["std"]
    )

    safe_std = max(
        baseline_std,
        1e-6,
    )

    drift_score = abs(
        rolling_mean - baseline_mean
    ) / safe_std

    return drift_score


def classify_drift_severity(
    drift_score: float,
) -> str | None:
    if drift_score >= ML_DRIFT_CRITICAL_THRESHOLD:
        return "critical"

    if drift_score >= ML_DRIFT_WARNING_THRESHOLD:
        return "warning"

    return None


def update_prediction_rates(
    result: str,
) -> None:
    normalized_result = result.lower()

    prediction_totals["total"] += 1

    if normalized_result == "fraud":
        prediction_totals["fraud"] += 1

    else:
        prediction_totals["legitimate"] += 1

    total = max(
        prediction_totals["total"],
        1,
    )

    fraud_rate = prediction_totals["fraud"] / total
    legitimate_rate = prediction_totals["legitimate"] / total

    ML_BUSINESS_FRAUD_RATE.set(
        fraud_rate
    )

    ML_BUSINESS_LEGITIMATE_RATE.set(
        legitimate_rate
    )

    ML_BUSINESS_PREDICTION_WINDOW_SIZE.set(
        min(
            prediction_totals["total"],
            ML_MONITORING_WINDOW_SIZE,
        )
    )


def record_business_ml_monitoring_metrics(
    engineered_features: dict[str, float],
    result: str,
    risk_level: str,
    model_version: str,
    fraud_probability: float,
) -> None:
    ML_BUSINESS_PREDICTIONS_TOTAL.labels(
        result=result,
        risk_level=risk_level,
        model_version=model_version,
    ).inc()

    update_prediction_rates(
        result=result
    )

    ML_BUSINESS_PROBABILITY_DISTRIBUTION.observe(
        fraud_probability
    )

    amount = float(
        engineered_features.get(
            "amount",
            0.0,
        )
    )

    total_business_risk_score = float(
        engineered_features.get(
            "total_business_risk_score",
            0.0,
        )
    )

    ML_BUSINESS_AMOUNT_DISTRIBUTION.observe(
        amount
    )

    ML_BUSINESS_RISK_SCORE_DISTRIBUTION.observe(
        total_business_risk_score
    )

    for feature_name in ML_MONITORED_FEATURES:
        raw_value = engineered_features.get(
            feature_name,
            0.0,
        )

        feature_value = float(raw_value)

        feature_windows[feature_name].append(
            feature_value
        )

        ML_BUSINESS_FEATURE_VALUE.labels(
            feature_name=feature_name,
        ).observe(feature_value)

        rolling_mean = calculate_rolling_mean(
            feature_windows[feature_name]
        )

        drift_score = calculate_feature_drift_score(
            feature_name=feature_name,
            rolling_mean=rolling_mean,
        )

        ML_BUSINESS_FEATURE_DRIFT_SCORE.labels(
            feature_name=feature_name,
        ).set(drift_score)

        severity = classify_drift_severity(
            drift_score=drift_score
        )

        if severity is not None:
            ML_BUSINESS_DRIFT_ALERTS_TOTAL.labels(
                feature_name=feature_name,
                severity=severity,
            ).inc()
