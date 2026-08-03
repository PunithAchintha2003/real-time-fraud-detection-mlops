from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import joblib
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from mlflow.tracking import MlflowClient
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

from src.config import (
    FEATURE_COLUMNS,
    MLFLOW_MODEL_ALIAS,
    MLFLOW_REGISTERED_MODEL_NAME,
)


MODEL_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODEL_DIR / "fraud_detection_model.joblib"
SCALER_PATH = MODEL_DIR / "scaler.joblib"

MLFLOW_DB_PATH = PROJECT_ROOT / "mlflow-ci.db"
MLFLOW_RUNS_PATH = PROJECT_ROOT / "mlruns-ci"


def reset_ci_mlflow_storage() -> None:
    if MLFLOW_DB_PATH.exists():
        MLFLOW_DB_PATH.unlink()

    if MLFLOW_RUNS_PATH.exists():
        shutil.rmtree(MLFLOW_RUNS_PATH)


def create_training_frame(rows: int = 800) -> pd.DataFrame:
    rng = np.random.default_rng(42)

    data = pd.DataFrame(
        rng.normal(
            loc=0.0,
            scale=1.0,
            size=(rows, len(FEATURE_COLUMNS)),
        ),
        columns=FEATURE_COLUMNS,
    )

    data["Time"] = rng.uniform(
        0,
        172800,
        size=rows,
    )

    data["Amount"] = rng.lognormal(
        mean=4.0,
        sigma=1.0,
        size=rows,
    )

    return data


def create_labels(data: pd.DataFrame) -> np.ndarray:
    rng = np.random.default_rng(7)

    risk_score = (
        0.00002 * data["Amount"]
        + 0.000001 * data["Time"]
        + 0.35 * data["V14"].abs()
        + 0.25 * data["V10"].abs()
        + rng.normal(
            0,
            0.2,
            size=len(data),
        )
    )

    labels = (
        risk_score
        > np.percentile(
            risk_score,
            80,
        )
    ).astype(int)

    return labels


def create_ci_model_artifacts() -> None:
    reset_ci_mlflow_storage()

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    tracking_uri = f"sqlite:///{MLFLOW_DB_PATH}"

    os.environ["MLFLOW_TRACKING_URI"] = tracking_uri

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_registry_uri(tracking_uri)

    data = create_training_frame()
    labels = create_labels(data)

    scaler = StandardScaler()

    scaled_data = data.copy()

    scaled_data[["Time", "Amount"]] = scaler.fit_transform(
        scaled_data[["Time", "Amount"]]
    )

    model = RandomForestClassifier(
        n_estimators=80,
        max_depth=8,
        random_state=42,
        class_weight="balanced",
    )

    model.fit(
        scaled_data[FEATURE_COLUMNS].to_numpy(),
        labels,
    )

    joblib.dump(
        model,
        MODEL_PATH,
    )

    joblib.dump(
        scaler,
        SCALER_PATH,
    )

    mlflow.set_experiment(
        "ci-fraud-detection"
    )

    with mlflow.start_run(
        run_name="ci-champion-model"
    ):
        mlflow.log_param(
            "model_type",
            "RandomForestClassifier",
        )

        mlflow.log_param(
            "purpose",
            "ci-test-artifact",
        )

        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            registered_model_name=MLFLOW_REGISTERED_MODEL_NAME,
        )

    client = MlflowClient(
        tracking_uri=tracking_uri,
        registry_uri=tracking_uri,
    )

    versions = client.search_model_versions(
        f"name='{MLFLOW_REGISTERED_MODEL_NAME}'"
    )

    latest_version = max(
        versions,
        key=lambda item: int(item.version),
    )

    client.set_registered_model_alias(
        name=MLFLOW_REGISTERED_MODEL_NAME,
        alias=MLFLOW_MODEL_ALIAS,
        version=latest_version.version,
    )

    print(f"CI MLflow tracking URI: {tracking_uri}")
    print(f"CI model saved to: {MODEL_PATH}")
    print(f"CI scaler saved to: {SCALER_PATH}")
    print(
        "CI MLflow champion registered: "
        f"{MLFLOW_REGISTERED_MODEL_NAME}@{MLFLOW_MODEL_ALIAS} "
        f"version {latest_version.version}"
    )


if __name__ == "__main__":
    create_ci_model_artifacts()
