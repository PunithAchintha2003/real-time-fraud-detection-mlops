import os

import joblib
import mlflow
import mlflow.sklearn

TRACKING_URI = os.environ["MLFLOW_TRACKING_URI"]
MODEL_PATH = "/app/models/business_fraud_model.joblib"
MODEL_NAME = "BusinessFraudDetectionModel"

mlflow.set_tracking_uri(TRACKING_URI)

artifact = joblib.load(MODEL_PATH)

if not isinstance(artifact, dict):
    raise TypeError(
        "Expected business_fraud_model.joblib to contain a dictionary artifact."
    )

model = artifact.get("model")

if model is None:
    raise ValueError(
        "Business model artifact does not contain a 'model' entry."
    )

if not hasattr(model, "predict_proba"):
    raise TypeError(
        "Business model entry does not expose predict_proba()."
    )

metrics = artifact.get("metrics", {})

with mlflow.start_run(
    run_name="local-register-BusinessFraudDetectionModel"
) as run:
    for metric_name in (
        "precision",
        "recall",
        "f1_score",
        "roc_auc",
    ):
        value = metrics.get(metric_name)

        if value is not None:
            mlflow.log_metric(
                metric_name,
                float(value),
            )

    mlflow.sklearn.log_model(
        sk_model=model,
        name="model",
        registered_model_name=MODEL_NAME,
    )

    client = mlflow.MlflowClient()

    versions = client.search_model_versions(
        f"name='{MODEL_NAME}'"
    )

    latest = max(
        versions,
        key=lambda version: int(version.version),
    )

    for key, value in artifact.items():
        if key in {
            "model",
            "metrics",
        }:
            continue

        if value is None:
            continue

        client.set_model_version_tag(
            MODEL_NAME,
            latest.version,
            key,
            str(value),
        )

    for metric_name, value in metrics.items():
        if value is None:
            continue

        client.set_model_version_tag(
            MODEL_NAME,
            latest.version,
            metric_name,
            str(value),
        )

    client.set_registered_model_alias(
        MODEL_NAME,
        "champion",
        latest.version,
    )

    print(
        f"Registered {MODEL_NAME} version={latest.version}"
    )
    print("Alias: champion")
    print(f"Run ID: {run.info.run_id}")
    print("BUSINESS_MODEL_REGISTRATION_SUCCESS")
