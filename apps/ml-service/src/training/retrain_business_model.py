from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

import joblib
import mlflow
import mlflow.sklearn
from mlflow import MlflowClient
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

from src.config import (
    BUSINESS_FRAUD_THRESHOLD,
    BUSINESS_MLFLOW_EXPERIMENT_NAME,
    BUSINESS_MLFLOW_MODEL_ALIAS,
    BUSINESS_MLFLOW_REGISTERED_MODEL_NAME,
    BUSINESS_MODEL_PATH,
    BUSINESS_RETRAINING_REPORT_PATH,
    MLFLOW_TRACKING_URI,
)
from src.features.business_features import FEATURE_COLUMNS
from src.training.train_business_model import (
    generate_synthetic_business_data,
)


def evaluate_model(
    model: RandomForestClassifier,
    x_test,
    y_test,
) -> dict[str, float]:
    probabilities = model.predict_proba(x_test)[:, 1]

    predictions = (
        probabilities >= BUSINESS_FRAUD_THRESHOLD
    ).astype(int)

    return {
        "precision": float(
            precision_score(
                y_test,
                predictions,
                zero_division=0,
            )
        ),
        "recall": float(
            recall_score(
                y_test,
                predictions,
                zero_division=0,
            )
        ),
        "f1_score": float(
            f1_score(
                y_test,
                predictions,
                zero_division=0,
            )
        ),
        "roc_auc": float(
            roc_auc_score(
                y_test,
                probabilities,
            )
        ),
    }


def get_champion(
    client: MlflowClient,
):
    try:
        return client.get_model_version_by_alias(
            name=BUSINESS_MLFLOW_REGISTERED_MODEL_NAME,
            alias=BUSINESS_MLFLOW_MODEL_ALIAS,
        )

    except Exception:
        return None


def get_champion_metrics(
    client: MlflowClient,
    champion,
) -> dict[str, float] | None:
    if champion is None:
        return None

    metrics: dict[str, float] = {}

    for metric_name in [
        "precision",
        "recall",
        "f1_score",
        "roc_auc",
    ]:
        raw_value = champion.tags.get(metric_name)

        if raw_value is not None:
            try:
                metrics[metric_name] = float(raw_value)
            except ValueError:
                pass

    if (
        "f1_score" in metrics
        and "roc_auc" in metrics
    ):
        return metrics

    run_id = champion.run_id

    if not run_id:
        return None

    try:
        run = client.get_run(run_id)

        for metric_name in [
            "precision",
            "recall",
            "f1_score",
            "roc_auc",
        ]:
            if metric_name in run.data.metrics:
                metrics[metric_name] = float(
                    run.data.metrics[metric_name]
                )

    except Exception:
        return None

    if (
        "f1_score" not in metrics
        or "roc_auc" not in metrics
    ):
        return None

    return metrics


def should_promote_candidate(
    candidate_metrics: dict[str, float],
    champion_metrics: dict[str, float] | None,
) -> tuple[bool, str]:
    if champion_metrics is None:
        return (
            True,
            "No existing champion with comparable metrics.",
        )

    candidate_f1 = candidate_metrics["f1_score"]
    candidate_roc_auc = candidate_metrics["roc_auc"]

    champion_f1 = champion_metrics["f1_score"]
    champion_roc_auc = champion_metrics["roc_auc"]

    if (
        candidate_f1 > champion_f1
        and candidate_roc_auc >= champion_roc_auc
    ):
        return (
            True,
            "Candidate passed the quality gate.",
        )

    return (
        False,
        (
            "Candidate rejected by quality gate. "
            "F1 must improve and ROC-AUC must not decrease."
        ),
    )


def save_retraining_report(
    report: dict[str, Any],
) -> None:
    BUSINESS_RETRAINING_REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    BUSINESS_RETRAINING_REPORT_PATH.write_text(
        json.dumps(
            report,
            indent=2,
        ),
        encoding="utf-8",
    )


def retrain_business_model() -> dict[str, Any]:
    mlflow.set_tracking_uri(
        MLFLOW_TRACKING_URI
    )

    mlflow.set_registry_uri(
        MLFLOW_TRACKING_URI
    )

    mlflow.set_experiment(
        BUSINESS_MLFLOW_EXPERIMENT_NAME
    )

    random_state = int(
        os.getenv(
            "BUSINESS_RETRAIN_RANDOM_STATE",
            datetime.now(timezone.utc).strftime("%Y%m%d"),
        )
    )

    rows = int(
        os.getenv(
            "BUSINESS_RETRAIN_ROWS",
            "25000",
        )
    )

    print("=" * 70)
    print("AUTOMATED BUSINESS FRAUD MODEL RETRAINING")
    print("=" * 70)

    print(
        f"Tracking URI : {MLFLOW_TRACKING_URI}"
    )

    print(
        "Registered model : "
        f"{BUSINESS_MLFLOW_REGISTERED_MODEL_NAME}"
    )

    print(
        f"Alias : @{BUSINESS_MLFLOW_MODEL_ALIAS}"
    )

    print(
        f"Training rows : {rows}"
    )

    print(
        f"Random state : {random_state}"
    )

    x, y = generate_synthetic_business_data(
        rows=rows,
        random_state=random_state,
    )

    x_train, x_test, y_train, y_test = (
        train_test_split(
            x,
            y,
            test_size=0.2,
            random_state=random_state,
            stratify=y,
        )
    )

    candidate_model = RandomForestClassifier(
        n_estimators=350,
        max_depth=14,
        min_samples_split=8,
        min_samples_leaf=3,
        class_weight="balanced",
        random_state=random_state,
        n_jobs=-1,
    )

    candidate_model.fit(
        x_train,
        y_train,
    )

    candidate_metrics = evaluate_model(
        candidate_model,
        x_test,
        y_test,
    )

    print("\nCandidate metrics:")

    for key, value in candidate_metrics.items():
        print(
            f"  {key:<10}: {value:.4f}"
        )

    client = MlflowClient(
        tracking_uri=MLFLOW_TRACKING_URI,
        registry_uri=MLFLOW_TRACKING_URI,
    )

    champion = get_champion(
        client
    )

    champion_metrics = get_champion_metrics(
        client,
        champion,
    )

    if champion is None:
        print(
            "\nNo existing business champion found."
        )

    else:
        print(
            "\nCurrent champion version: "
            f"{champion.version}"
        )

        if champion_metrics is not None:
            print(
                "Current champion F1: "
                f"{champion_metrics['f1_score']:.4f}"
            )

            print(
                "Current champion ROC-AUC: "
                f"{champion_metrics['roc_auc']:.4f}"
            )

    promoted = False
    registered_version: str | None = None

    with mlflow.start_run(
        run_name=(
            "business-fraud-retrain-"
            f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
        )
    ) as run:
        mlflow.log_param(
            "model_type",
            "RandomForestClassifier",
        )

        mlflow.log_param(
            "rows",
            rows,
        )

        mlflow.log_param(
            "random_state",
            random_state,
        )

        mlflow.log_param(
            "threshold",
            BUSINESS_FRAUD_THRESHOLD,
        )

        mlflow.log_param(
            "feature_count",
            len(FEATURE_COLUMNS),
        )

        mlflow.log_metrics(
            candidate_metrics
        )

        model_info = mlflow.sklearn.log_model(
            sk_model=candidate_model,
            name="model",
        )

        promote, reason = should_promote_candidate(
            candidate_metrics,
            champion_metrics,
        )

        mlflow.set_tag(
            "promotion_decision",
            (
                "promoted"
                if promote
                else "rejected"
            ),
        )

        mlflow.set_tag(
            "promotion_reason",
            reason,
        )

        if promote:
            logged_model_id = getattr(
                model_info,
                "model_id",
                None,
            )

            if not logged_model_id:
                raise RuntimeError(
                    "MLflow did not return a logged model ID."
                )

            model_version = mlflow.register_model(
                model_uri=(
                    f"models:/{logged_model_id}"
                ),
                name=BUSINESS_MLFLOW_REGISTERED_MODEL_NAME,
            )

            registered_version = str(
                model_version.version
            )

            for (
                metric_name,
                metric_value,
            ) in candidate_metrics.items():
                client.set_model_version_tag(
                    name=BUSINESS_MLFLOW_REGISTERED_MODEL_NAME,
                    version=registered_version,
                    key=metric_name,
                    value=str(metric_value),
                )

            client.set_model_version_tag(
                name=BUSINESS_MLFLOW_REGISTERED_MODEL_NAME,
                version=registered_version,
                key="training_rows",
                value=str(rows),
            )

            client.set_model_version_tag(
                name=BUSINESS_MLFLOW_REGISTERED_MODEL_NAME,
                version=registered_version,
                key="random_state",
                value=str(random_state),
            )

            client.set_registered_model_alias(
                name=BUSINESS_MLFLOW_REGISTERED_MODEL_NAME,
                alias=BUSINESS_MLFLOW_MODEL_ALIAS,
                version=registered_version,
            )

            artifact = {
                "model": candidate_model,
                "feature_columns": FEATURE_COLUMNS,
                "threshold": BUSINESS_FRAUD_THRESHOLD,
                "model_type": "RandomForestClassifier",
                "model_version": registered_version,
                "model_source": "mlflow",
                "created_at": (
                    datetime.now(
                        timezone.utc
                    ).isoformat()
                ),
                "metrics": {
                    key: round(
                        value,
                        4,
                    )
                    for key, value
                    in candidate_metrics.items()
                },
            }

            BUSINESS_MODEL_PATH.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            temporary_model_path = (
                BUSINESS_MODEL_PATH.with_name(
                    BUSINESS_MODEL_PATH.name + ".tmp"
                )
            )

            try:
                joblib.dump(
                    artifact,
                    temporary_model_path,
                )

                os.replace(
                    temporary_model_path,
                    BUSINESS_MODEL_PATH,
                )

            finally:
                if temporary_model_path.exists():
                    temporary_model_path.unlink()

            promoted = True

            print(
                "\nCandidate PROMOTED."
            )

            print(
                "New champion version: "
                f"{registered_version}"
            )

        else:
            print(
                "\nCandidate REJECTED."
            )

            print(reason)

        report = {
            "timestamp": (
                datetime.now(
                    timezone.utc
                ).isoformat()
            ),
            "run_id": run.info.run_id,
            "registered_model": (
                BUSINESS_MLFLOW_REGISTERED_MODEL_NAME
            ),
            "model_alias": (
                BUSINESS_MLFLOW_MODEL_ALIAS
            ),
            "candidate_metrics": {
                key: round(
                    value,
                    6,
                )
                for key, value
                in candidate_metrics.items()
            },
            "previous_champion_version": (
                str(champion.version)
                if champion is not None
                else None
            ),
            "previous_champion_metrics": (
                champion_metrics
            ),
            "promoted": promoted,
            "registered_version": (
                registered_version
            ),
            "reason": reason,
            "rows": rows,
            "random_state": random_state,
        }

        save_retraining_report(
            report
        )

    print(
        "\nRetraining report saved to:"
    )

    print(
        BUSINESS_RETRAINING_REPORT_PATH
    )

    print("=" * 70)

    return report


if __name__ == "__main__":
    retrain_business_model()
