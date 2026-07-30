from typing import Dict, Any, Optional, Tuple

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd

from mlflow import MlflowClient

from src.config import (
    FRAUD_THRESHOLD,
    MLFLOW_MODEL_ALIAS,
    MLFLOW_REGISTERED_MODEL_NAME,
    MLFLOW_TRACKING_URI,
    MODEL_PATH,
    SCALER_PATH,
    FEATURE_COLUMNS,
)

from src.data.preprocessing import preprocess_features


# MLFLOW CONFIGURATION

mlflow.set_tracking_uri(
    MLFLOW_TRACKING_URI
)


# LOAD MODEL FROM MLFLOW

def load_model_from_mlflow() -> Tuple[Any, Optional[str]]:
    """
    Load the current Champion model from MLflow Model Registry.

    Returns:
        Tuple containing:
            - Loaded MLflow model
            - Model version as a string
    """

    # Create MLflow model URI using the Champion alias

    model_uri = (
        f"models:/"
        f"{MLFLOW_REGISTERED_MODEL_NAME}"
        f"@{MLFLOW_MODEL_ALIAS}"
    )

    print(
        f"Loading model from MLflow: {model_uri}"
    )

    # Create MLflow client

    client = MlflowClient(
        tracking_uri=MLFLOW_TRACKING_URI
    )

    # Get Champion model version

    model_version_info = (
        client.get_model_version_by_alias(
            name=MLFLOW_REGISTERED_MODEL_NAME,
            alias=MLFLOW_MODEL_ALIAS,
        )
    )

    model_version = str(
        model_version_info.version
    )

    print(
        "Champion model version: "
        f"{model_version}"
    )

    # Load model from MLflow

    model = mlflow.sklearn.load_model(
        model_uri
    )

    return (
        model,
        model_version,
    )

# LOAD LOCAL MODEL

def load_local_model():
    """
    Load the locally saved model.

    This model is used as a fallback if the
    MLflow Champion model cannot be loaded.

    Returns:
        Locally loaded machine learning model.
    """

    if not MODEL_PATH.exists():

        raise FileNotFoundError(
            f"Local model not found at: "
            f"{MODEL_PATH}"
        )

    model = joblib.load(
        MODEL_PATH
    )

    return model


# PUBLIC MODEL LOADING FUNCTION

def load_model():
    """
    Load the fraud detection model.

    MLflow Champion model is the primary source.

    If MLflow model loading fails,
    the locally saved joblib model is used
    as a fallback.

    Returns:
        Loaded machine learning model.
    """

    try:

        model, _ = load_model_from_mlflow()

        return model

    except Exception as error:

        print(
            "WARNING: Failed to load model "
            f"from MLflow: {error}"
        )

        print(
            "Loading local model as fallback..."
        )

        return load_local_model()


# LOAD SCALER

def load_scaler():
    """
    Load the fitted StandardScaler.

    The scaler must be the same scaler that
    was fitted during model training.

    Returns:
        Loaded scaler.
    """

    if not SCALER_PATH.exists():

        raise FileNotFoundError(
            f"Scaler not found at: "
            f"{SCALER_PATH}"
        )

    scaler = joblib.load(
        SCALER_PATH
    )

    return scaler


# INFERENCE SERVICE

class FraudDetectionService:
    """
    Service responsible for:

    - Loading the MLflow Champion model
    - Falling back to the local model
    - Loading the fitted scaler
    - Preprocessing transaction data
    - Generating fraud predictions
    """

    def __init__(self):

        self.model = None

        self.scaler = None

        self.model_version = None

        self.model_source = None

        self.is_ready = False


    # LOAD MODEL AND SCALER

    def load(self):
        """
        Load the MLflow Champion model and scaler.

        MLflow Champion model is the primary source.

        Local joblib model is used as fallback
        if MLflow loading fails.

        The service is marked as ready only after
        both model and scaler are successfully loaded.
        """

        # Reset readiness before loading

        self.is_ready = False

        # TRY TO LOAD MLFLOW CHAMPION MODEL

        try:

            (
                self.model,
                self.model_version,
            ) = load_model_from_mlflow()

            self.model_source = "mlflow"

            print(
                "Champion model loaded "
                "successfully from MLflow."
            )

            print(
                f"Model version: "
                f"{self.model_version}"
            )

        except Exception as error:

            print(
                "WARNING: Failed to load "
                "Champion model from MLflow: "
                f"{error}"
            )

            print(
                "Attempting to load local model..."
            )

            # FALLBACK TO LOCAL MODEL

            self.model = load_local_model()

            self.model_version = None

            self.model_source = "local"

            print(
                "Local model loaded successfully."
            )


        # LOAD SCALER

        self.scaler = load_scaler()

        print(
            "Scaler loaded successfully."
        )


        # MARK SERVICE AS READY

        self.is_ready = True

        print(
            "Fraud detection service is ready."
        )

    # PREDICT

    def predict(
        self,
        transaction: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate a fraud prediction for a transaction.

        Args:
            transaction:
                Dictionary containing all required
                transaction features.

        Returns:
            Dictionary containing:

            - prediction
            - is_fraud
            - fraud_probability
            - threshold
            - result
            - model_source
            - model_version
        """

        # CHECK SERVICE READINESS

        if not self.is_ready:

            raise RuntimeError(
                "Fraud detection service "
                "is not ready."
            )


        # VALIDATE REQUIRED FEATURES

        missing_features = [
            feature
            for feature in FEATURE_COLUMNS
            if feature not in transaction
        ]

        if missing_features:

            raise ValueError(
                "Missing required features: "
                + ", ".join(
                    missing_features
                )
            )


        # CREATE INPUT DATAFRAME

        input_data = pd.DataFrame(
            [
                [
                    transaction[feature]
                    for feature in FEATURE_COLUMNS
                ]
            ],
            columns=FEATURE_COLUMNS,
        )


        # PREPROCESS INPUT

        processed_data = preprocess_features(
            input_data,
            self.scaler,
            fit_scaler=False,
        )


        # GENERATE FRAUD PROBABILITY

        fraud_probability = (
            self.model.predict_proba(
                processed_data
            )[0][1]
        )

        fraud_probability = float(
            fraud_probability
        )


        # APPLY FRAUD THRESHOLD

        prediction = int(
            fraud_probability
            >= FRAUD_THRESHOLD
        )


        # RETURN PREDICTION RESULT

        return {

            "prediction": prediction,

            "is_fraud": bool(
                prediction == 1
            ),

            "fraud_probability": round(
                fraud_probability,
                6,
            ),

            "threshold": FRAUD_THRESHOLD,

            "result": (
                "Fraudulent"
                if prediction == 1
                else "Legitimate"
            ),

            "model_source": (
                self.model_source
            ),

            "model_version": (
                str(
                    self.model_version
                )
                if self.model_version is not None
                else None
            ),
        }


# GLOBAL INFERENCE SERVICE

fraud_detection_service = (
    FraudDetectionService()
)


# PUBLIC PREDICTION FUNCTION

def predict_transaction(
    transaction: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Public prediction function.

    Used by:

    - Unit tests
    - FastAPI
    - Other inference clients

    Automatically loads the inference service
    if it has not already been initialized.
    """

    if not fraud_detection_service.is_ready:

        fraud_detection_service.load()

    return (
        fraud_detection_service.predict(
            transaction
        )
    )


# SAMPLE TRANSACTION

SAMPLE_TRANSACTION = {

    "Time": 406,

    "V1": -1.359807,

    "V2": -0.072781,

    "V3": 2.536347,

    "V4": 1.378155,

    "V5": -0.338321,

    "V6": 0.462388,

    "V7": 0.239599,

    "V8": 0.098698,

    "V9": 0.363787,

    "V10": 0.090794,

    "V11": -0.551600,

    "V12": -0.617801,

    "V13": -0.991390,

    "V14": -0.311169,

    "V15": 1.468177,

    "V16": -0.470400,

    "V17": 0.207971,

    "V18": 0.025791,

    "V19": 0.403993,

    "V20": 0.251412,

    "V21": -0.018307,

    "V22": 0.277838,

    "V23": -0.110474,

    "V24": 0.066928,

    "V25": 0.128539,

    "V26": -0.189115,

    "V27": 0.133558,

    "V28": -0.021053,

    "Amount": 149.62,
}


# MAIN

def main():

    print("=" * 60)

    print(
        "REAL-TIME FRAUD DETECTION"
    )

    print(
        "MODEL INFERENCE PIPELINE"
    )

    print("=" * 60)


    # LOAD INFERENCE SERVICE

    print(
        "\nLoading fraud detection service..."
    )

    fraud_detection_service.load()


    # GENERATE PREDICTION

    print(
        "\nGenerating prediction..."
    )

    result = predict_transaction(
        SAMPLE_TRANSACTION
    )


    # DISPLAY RESULT

    print(
        "\n" + "=" * 60
    )

    print(
        "PREDICTION RESULT"
    )

    print(
        "=" * 60
    )

    for key, value in result.items():

        print(
            f"{key:<20}: {value}"
        )


# APPLICATION ENTRY POINT

if __name__ == "__main__":

    main()