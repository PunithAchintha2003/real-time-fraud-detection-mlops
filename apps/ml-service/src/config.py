from pathlib import Path
import os


# PROJECT PATHS

# Project root directory
# src/config.py -> src -> project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]


# DATA PATHS

DATA_DIR = PROJECT_ROOT / "data"

DATA_PATH = DATA_DIR / "creditcard.csv"


# LOCAL MODEL PATHS

MODELS_DIR = PROJECT_ROOT / "models"

MODEL_PATH = (
    MODELS_DIR / "fraud_detection_model.joblib"
)

SCALER_PATH = (
    MODELS_DIR / "scaler.joblib"
)


# MLFLOW LOCAL PATHS

MLFLOW_DB_PATH = (
    PROJECT_ROOT / "mlflow.db"
)

MLFLOW_ARTIFACTS_DIR = (
    PROJECT_ROOT / "mlruns"
)


# MLFLOW CONFIGURATION

# Docker:
#   http://mlflow-server:5000
#
# Local:
#   sqlite:///.../mlflow.db
#
# When MLFLOW_TRACKING_URI is provided through
# Docker Compose or environment variables, it will
# automatically override the local default.

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


# MLFLOW ARTIFACT CONFIGURATION

# This path is mainly used by the MLflow server.
#
# Docker MLflow server:
#   /mlflow/mlruns
#
# Docker host:
#   ./mlruns
#
# Local development:
#   PROJECT_ROOT / "mlruns"

MLFLOW_ARTIFACT_ROOT = os.getenv(
    "MLFLOW_ARTIFACT_ROOT",
    str(MLFLOW_ARTIFACTS_DIR)
)


# MODEL CONFIGURATION

# Probability threshold used to classify
# a transaction as fraudulent.

FRAUD_THRESHOLD = float(
    os.getenv(
        "FRAUD_THRESHOLD",
        "0.5"
    )
)


# MODEL FEATURES

# The trained model expects exactly 30 features.
#
# IMPORTANT:
# The order must remain identical during:
#
# 1. Training
# 2. Model evaluation
# 3. API inference

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


# SCALED FEATURES

# Only these features are scaled.
#
# The same fitted StandardScaler must be used
# during training and inference.

SCALED_FEATURES = [
    "Time",
    "Amount",
]