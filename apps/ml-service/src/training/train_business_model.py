from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

from src.features.business_features import (
    FEATURE_COLUMNS,
    make_business_features,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODEL_DIR / "business_fraud_model.joblib"
REPORT_PATH = MODEL_DIR / "business_fraud_model_report.json"


MERCHANT_TYPES = [
    "grocery",
    "restaurant",
    "fuel",
    "online_purchase",
    "electronics",
    "travel",
    "digital_goods",
    "crypto",
    "gaming",
    "other",
]


LOCATIONS = [
    "sri_lanka",
    "india",
    "uae",
    "singapore",
    "united_kingdom",
    "united_states",
    "nigeria",
    "unknown",
    "other",
]


PAYMENT_METHODS = [
    "card",
    "bank_transfer",
    "wallet",
    "crypto",
    "cash",
    "other",
]


DEVICE_TYPES = [
    "mobile",
    "desktop",
    "tablet",
    "unknown",
    "other",
]


def sigmoid(value: float) -> float:
    return 1.0 / (1.0 + np.exp(-value))


def generate_synthetic_business_data(
    rows: int = 25000,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.Series]:
    rng = np.random.default_rng(random_state)

    records: list[dict[str, float]] = []
    labels: list[int] = []

    for _ in range(rows):
        amount = float(
            np.clip(
                rng.lognormal(mean=4.7, sigma=1.1),
                1,
                10000,
            )
        )

        merchant_type = str(
            rng.choice(
                MERCHANT_TYPES,
                p=[
                    0.18,
                    0.14,
                    0.10,
                    0.22,
                    0.10,
                    0.08,
                    0.06,
                    0.03,
                    0.05,
                    0.04,
                ],
            )
        )

        location = str(
            rng.choice(
                LOCATIONS,
                p=[
                    0.42,
                    0.12,
                    0.10,
                    0.06,
                    0.08,
                    0.08,
                    0.03,
                    0.04,
                    0.07,
                ],
            )
        )

        payment_method = str(
            rng.choice(
                PAYMENT_METHODS,
                p=[
                    0.48,
                    0.18,
                    0.18,
                    0.03,
                    0.08,
                    0.05,
                ],
            )
        )

        device_type = str(
            rng.choice(
                DEVICE_TYPES,
                p=[
                    0.56,
                    0.30,
                    0.06,
                    0.04,
                    0.04,
                ],
            )
        )

        hour = int(rng.integers(0, 24))

        is_international = bool(
            rng.choice(
                [False, True],
                p=[0.82, 0.18],
            )
        )

        previous_failed_attempts = int(
            min(
                rng.poisson(lam=0.35),
                8,
            )
        )

        transaction = {
            "amount": amount,
            "merchant_type": merchant_type,
            "location": location,
            "transaction_time": f"{hour:02d}:00",
            "payment_method": payment_method,
            "device_type": device_type,
            "is_international": is_international,
            "previous_failed_attempts": previous_failed_attempts,
        }

        features = make_business_features(transaction)

        risk_signal = (
            -3.1
            + 3.2 * features["total_business_risk_score"]
            + 0.65 * features["failed_attempt_risk"]
            + 0.45 * features["is_international"]
            + 0.35 * features["is_night_transaction"]
            + 0.25 * features["amount_risk_score"]
        )

        fraud_probability = sigmoid(risk_signal)

        label = int(rng.random() < fraud_probability)

        records.append(features)
        labels.append(label)

    x = pd.DataFrame(records, columns=FEATURE_COLUMNS)
    y = pd.Series(labels, name="is_fraud")

    return x, y


def train_business_model() -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    x, y = generate_synthetic_business_data()

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=350,
        max_depth=14,
        min_samples_split=8,
        min_samples_leaf=3,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )

    model.fit(x_train, y_train)

    probabilities = model.predict_proba(x_test)[:, 1]

    threshold = 0.50
    predictions = (probabilities >= threshold).astype(int)

    metrics = {
        "precision": round(
            precision_score(y_test, predictions, zero_division=0),
            4,
        ),
        "recall": round(
            recall_score(y_test, predictions, zero_division=0),
            4,
        ),
        "f1_score": round(
            f1_score(y_test, predictions, zero_division=0),
            4,
        ),
        "roc_auc": round(
            roc_auc_score(y_test, probabilities),
            4,
        ),
        "fraud_rate": round(
            float(y.mean()),
            4,
        ),
        "rows": int(len(x)),
        "features": FEATURE_COLUMNS,
        "classification_report": classification_report(
            y_test,
            predictions,
            zero_division=0,
            output_dict=True,
        ),
    }

    artifact = {
        "model": model,
        "feature_columns": FEATURE_COLUMNS,
        "threshold": threshold,
        "model_type": "RandomForestClassifier",
        "model_version": "business-v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "metrics": metrics,
    }

    joblib.dump(
        artifact,
        MODEL_PATH,
    )

    REPORT_PATH.write_text(
        json.dumps(metrics, indent=2),
        encoding="utf-8",
    )

    print("Business fraud model trained successfully.")
    print(f"Model saved to: {MODEL_PATH}")
    print(f"Report saved to: {REPORT_PATH}")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    train_business_model()