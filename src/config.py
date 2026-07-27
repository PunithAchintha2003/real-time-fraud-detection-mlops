from pathlib import Path
import os


# PROJECT PATHS

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Dataset directory
DATA_DIR = PROJECT_ROOT / "data"

# Dataset path
DATA_PATH = DATA_DIR / "creditcard.csv"

# Models directory
MODELS_DIR = PROJECT_ROOT / "models"

# Local model artifact
MODEL_PATH = MODELS_DIR / "fraud_detection_model.joblib"

# Local scaler artifact
SCALER_PATH = MODELS_DIR / "scaler.joblib"

# MLflow SQLite database
MLFLOW_DB_PATH = PROJECT_ROOT / "mlflow.db"


# MLFLOW CONFIGURATION

MLFLOW_TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI",
    f"sqlite:///{MLFLOW_DB_PATH}"
)

MLFLOW_EXPERIMENT_NAME = os.getenv(
    "MLFLOW_EXPERIMENT_NAME",
    "fraud-detection-model-comparison"
)

MLFLOW_REGISTERED_MODEL_NAME = os.getenv(
    "MLFLOW_REGISTERED_MODEL_NAME",
    "FraudDetectionModel"
)

MLFLOW_MODEL_ALIAS = os.getenv(
    "MLFLOW_MODEL_ALIAS",
    "champion"
)


# MODEL CONFIGURATION

# Fraud classification threshold.
#
# Default:
# 0.5
#
# Later you can tune this value based on
# precision/recall requirements.
FRAUD_THRESHOLD = float(
    os.getenv(
        "FRAUD_THRESHOLD",
        "0.5"
    )
)


# MODEL FEATURES

# The model expects exactly 30 features.
#
# IMPORTANT:
# The order must remain exactly the same
# during training and inference.

FEATURE_COLUMNS = [
    "Time",
    "V1",
    "V2",
    "V3",
    "V4",
    "V5",
    "V6",
    "V7",
    "V8",
    "V9",
    "V10",
    "V11",
    "V12",
    "V13",
    "V14",
    "V15",
    "V16",
    "V17",
    "V18",
    "V19",
    "V20",
    "V21",
    "V22",
    "V23",
    "V24",
    "V25",
    "V26",
    "V27",
    "V28",
    "Amount",
]


# Features that were scaled during training
SCALED_FEATURES = [
    "Time",
    "Amount",
]