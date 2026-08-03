from __future__ import annotations

import math
from typing import Any

import pandas as pd


FEATURE_COLUMNS = [
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


MERCHANT_RISK_SCORES = {
    "grocery": 0.10,
    "restaurant": 0.18,
    "fuel": 0.22,
    "online_purchase": 0.45,
    "electronics": 0.55,
    "travel": 0.50,
    "digital_goods": 0.75,
    "crypto": 0.90,
    "gaming": 0.65,
    "other": 0.35,
}


LOCATION_RISK_SCORES = {
    "sri_lanka": 0.15,
    "india": 0.28,
    "uae": 0.22,
    "singapore": 0.20,
    "united_kingdom": 0.24,
    "united_states": 0.30,
    "nigeria": 0.78,
    "unknown": 0.85,
    "other": 0.45,
}


PAYMENT_METHOD_RISK_SCORES = {
    "card": 0.25,
    "bank_transfer": 0.18,
    "wallet": 0.35,
    "crypto": 0.90,
    "cash": 0.12,
    "other": 0.40,
}


DEVICE_RISK_SCORES = {
    "mobile": 0.25,
    "desktop": 0.18,
    "tablet": 0.22,
    "unknown": 0.80,
    "other": 0.40,
}


def normalize_category(value: Any) -> str:
    if value is None:
        return "unknown"

    return (
        str(value)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )


def parse_hour(transaction_time: Any) -> float:
    if transaction_time is None:
        return 0.0

    value = str(transaction_time).strip()

    if ":" in value:
        hour_text = value.split(":")[0]

        try:
            hour = int(hour_text)
            return float(max(0, min(hour, 23)))
        except ValueError:
            return 0.0

    try:
        hour = int(float(value))
        return float(max(0, min(hour, 23)))
    except ValueError:
        return 0.0


def calculate_amount_risk(amount: float) -> float:
    if amount <= 0:
        return 0.10

    if amount < 50:
        return 0.15

    if amount < 250:
        return 0.25

    if amount < 1000:
        return 0.45

    if amount < 5000:
        return 0.70

    return 0.90


def make_business_features(transaction: dict[str, Any]) -> dict[str, float]:
    amount = float(transaction.get("amount", 0) or 0)

    merchant_type = normalize_category(
        transaction.get("merchant_type", "other")
    )

    location = normalize_category(
        transaction.get("location", "other")
    )

    payment_method = normalize_category(
        transaction.get("payment_method", "other")
    )

    device_type = normalize_category(
        transaction.get("device_type", "other")
    )

    hour = parse_hour(transaction.get("transaction_time", "00:00"))

    is_night_transaction = 1.0 if hour < 6 or hour >= 22 else 0.0

    is_international = 1.0 if bool(
        transaction.get("is_international", False)
    ) else 0.0

    previous_failed_attempts = float(
        transaction.get("previous_failed_attempts", 0) or 0
    )

    failed_attempt_risk = min(previous_failed_attempts / 5.0, 1.0)

    merchant_risk_score = MERCHANT_RISK_SCORES.get(
        merchant_type,
        MERCHANT_RISK_SCORES["other"],
    )

    location_risk_score = LOCATION_RISK_SCORES.get(
        location,
        LOCATION_RISK_SCORES["other"],
    )

    payment_method_risk = PAYMENT_METHOD_RISK_SCORES.get(
        payment_method,
        PAYMENT_METHOD_RISK_SCORES["other"],
    )

    device_risk_score = DEVICE_RISK_SCORES.get(
        device_type,
        DEVICE_RISK_SCORES["other"],
    )

    amount_risk_score = calculate_amount_risk(amount)

    total_business_risk_score = (
        0.20 * merchant_risk_score
        + 0.15 * location_risk_score
        + 0.15 * payment_method_risk
        + 0.10 * device_risk_score
        + 0.15 * is_international
        + 0.10 * is_night_transaction
        + 0.10 * failed_attempt_risk
        + 0.05 * amount_risk_score
    )

    return {
        "amount": amount,
        "log_amount": math.log1p(max(amount, 0)),
        "hour": hour,
        "is_night_transaction": is_night_transaction,
        "merchant_risk_score": merchant_risk_score,
        "location_risk_score": location_risk_score,
        "payment_method_risk": payment_method_risk,
        "device_risk_score": device_risk_score,
        "is_international": is_international,
        "previous_failed_attempts": previous_failed_attempts,
        "failed_attempt_risk": failed_attempt_risk,
        "amount_risk_score": amount_risk_score,
        "total_business_risk_score": total_business_risk_score,
    }


def make_business_feature_frame(transaction: dict[str, Any]) -> pd.DataFrame:
    features = make_business_features(transaction)

    return pd.DataFrame(
        [[features[column] for column in FEATURE_COLUMNS]],
        columns=FEATURE_COLUMNS,
    )