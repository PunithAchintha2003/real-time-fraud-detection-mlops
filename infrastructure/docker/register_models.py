import glob
import os
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn


TRACKING_URI = os.environ["MLFLOW_TRACKING_URI"]
MODEL_DIR = Path("/app/models")

mlflow.set_tracking_uri(TRACKING_URI)

client = mlflow.MlflowClient()


def is_predictive_model(path: str) -> bool:
    try:
        obj = joblib.load(path)
        return hasattr(obj, "predict_proba") and hasattr(obj, "predict")
    except Exception:
        return False


def register_model(model_path: str, model_name: str) -> None:
    print(f"Registering {model_name} from {model_path}")

    model = joblib.load(model_path)

    with mlflow.start_run(run_name=f"cloud-import-{model_name}") as run:
        mlflow.sklearn.log_model(
            sk_model=model,
            name="model",
            registered_model_name=model_name,
        )

        versions = client.search_model_versions(
            f"name='{model_name}'"
        )

        latest = max(
            versions,
            key=lambda version: int(version.version),
        )

        client.set_registered_model_alias(
            model_name,
            "champion",
            latest.version,
        )

        print(
            f"Registered {model_name} "
            f"version={latest.version} "
            f"alias=champion "
            f"run={run.info.run_id}"
        )


business_model = MODEL_DIR / "business_fraud_model.joblib"

if not business_model.exists():
    raise FileNotFoundError(
        f"Business model not found: {business_model}"
    )

fraud_candidates = [
    path
    for path in glob.glob(str(MODEL_DIR / "*.joblib"))
    if Path(path).name != business_model.name
    and is_predictive_model(path)
]

if not fraud_candidates:
    raise FileNotFoundError(
        "Could not find the fraud prediction model in /app/models"
    )

fraud_model = fraud_candidates[0]

print("MLflow tracking URI:", TRACKING_URI)
print("Fraud model:", fraud_model)
print("Business model:", business_model)

register_model(
    fraud_model,
    "FraudDetectionModel",
)

register_model(
    str(business_model),
    "BusinessFraudDetectionModel",
)

print("MODEL_REGISTRATION_SUCCESS")
