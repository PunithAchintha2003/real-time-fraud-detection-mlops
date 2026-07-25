from pathlib import Path

import joblib
import pandas as pd


# PROJECT CONFIGURATION

# Root directory of the project
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Directory containing trained model artifacts
MODELS_DIR = PROJECT_ROOT / "models"

# Path to the trained fraud detection model
MODEL_PATH = MODELS_DIR / "fraud_detection_model.joblib"

# Path to the fitted StandardScaler
SCALER_PATH = MODELS_DIR / "scaler.joblib"


# MODEL LOADING

def load_model():
    """
    Load the trained fraud detection model from disk.

    Returns:
        Trained machine learning model.
    """

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Trained model not found at: {MODEL_PATH}"
        )

    model = joblib.load(MODEL_PATH)

    return model


def load_scaler():
    """
    Load the fitted StandardScaler from disk.

    Returns:
        Fitted StandardScaler instance.
    """

    if not SCALER_PATH.exists():
        raise FileNotFoundError(
            f"Scaler not found at: {SCALER_PATH}"
        )

    scaler = joblib.load(SCALER_PATH)

    return scaler


# PREPROCESS INPUT DATA

def preprocess_input(transaction, scaler):
    """
    Preprocess a single transaction before prediction.

    The preprocessing must match the preprocessing
    performed during model training.

    Args:
        transaction (dict):
            Transaction data containing all model features.

        scaler:
            Fitted StandardScaler used during training.

    Returns:
        pandas.DataFrame:
            Preprocessed transaction ready for prediction.
    """

    # Convert transaction dictionary into a DataFrame
    input_data = pd.DataFrame([transaction])

    # Validate required features
    required_features = [
        "Time",
        "Amount"
    ]

    for feature in required_features:
        if feature not in input_data.columns:
            raise ValueError(
                f"Missing required feature: {feature}"
            )

    # Apply the same scaling used during model training
    input_data[["Time", "Amount"]] = scaler.transform(
        input_data[["Time", "Amount"]]
    )

    return input_data


# FRAUD PREDICTION

def predict_transaction(transaction):
    """
    Predict whether a transaction is fraudulent.

    Args:
        transaction (dict):
            Transaction feature values.

    Returns:
        dict:
            Prediction result containing:
            - prediction
            - fraud_probability
            - is_fraud
    """

    # Load trained model
    model = load_model()

    # Load fitted scaler
    scaler = load_scaler()

    # Preprocess input transaction
    processed_data = preprocess_input(
        transaction,
        scaler
    )

    # Generate class prediction
    prediction = model.predict(
        processed_data
    )[0]

    # Generate probability of fraud
    fraud_probability = model.predict_proba(
        processed_data
    )[0][1]

    # Convert numerical prediction to readable label
    if prediction == 1:
        prediction_label = "Fraud"
    else:
        prediction_label = "Legitimate"

    # Return structured prediction result
    return {
        "prediction": prediction_label,
        "fraud_probability": round(
            float(fraud_probability),
            4
        ),
        "is_fraud": bool(prediction)
    }


# MAIN

def main():
    """
    Run a sample fraud detection prediction.
    """

    print("=" * 60)
    print("REAL-TIME FRAUD DETECTION")
    print("MODEL INFERENCE PIPELINE")
    print("=" * 60)

    print("\nLoading trained model...")

    # Load model
    model = load_model()

    print(
        f"Model loaded successfully from: {MODEL_PATH}"
    )

    print("\nLoading scaler...")

    # Load scaler
    scaler = load_scaler()

    print(
        f"Scaler loaded successfully from: {SCALER_PATH}"
    )

    # Create sample transaction
    #
    # IMPORTANT:
    # These are example values only.
    # The transaction must contain all 30 features
    # expected by the trained model.

    sample_transaction = {
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
        "Amount": 149.62
    }

    print("\nGenerating prediction...")

    # Generate fraud prediction
    result = predict_transaction(
        sample_transaction
    )

    # Display prediction result
    print("\n" + "=" * 60)
    print("PREDICTION RESULT")
    print("=" * 60)

    print(
        f"Prediction         : {result['prediction']}"
    )

    print(
        f"Fraud Probability  : "
        f"{result['fraud_probability']:.4f}"
    )

    print(
        f"Is Fraud           : {result['is_fraud']}"
    )

    print(
        "\nModel inference completed successfully."
    )


if __name__ == "__main__":
    main()