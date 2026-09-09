import os
import joblib
import mlflow
import mlflow.sklearn

TRACKING_URI = os.environ["MLFLOW_TRACKING_URI"]
MODEL_PATH = "/app/models/business_fraud_model.joblib"
MODEL_NAME = "BusinessFraudDetectionModel"

mlflow.set_tracking_uri(TRACKING_URI)

model = joblib.load(MODEL_PATH)

with mlflow.start_run(run_name="cloud-import-BusinessFraudDetectionModel") as run:
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

    client.set_registered_model_alias(
        MODEL_NAME,
        "champion",
        latest.version,
    )

    print(f"Registered {MODEL_NAME} version={latest.version}")
    print("Alias: champion")
    print(f"Run ID: {run.info.run_id}")
    print("BUSINESS_MODEL_REGISTRATION_SUCCESS")
