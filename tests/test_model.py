import pytest

from src.inference.predict import (
    load_model,
    load_scaler,
    predict_transaction,
    fraud_detection_service,
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


# LOAD INFERENCE SERVICE BEFORE TESTS

@pytest.fixture(
    scope="module",
    autouse=True
)
def setup_inference_service():
    """
    Load the MLflow champion model and scaler
    before running model inference tests.
    """

    if not fraud_detection_service.is_ready:

        fraud_detection_service.load()


# TEST MODEL LOADING

def test_model_loading():

    model = load_model()

    assert model is not None

    assert hasattr(
        model,
        "predict"
    )

    assert hasattr(
        model,
        "predict_proba"
    )


# TEST SCALER LOADING

def test_scaler_loading():

    scaler = load_scaler()

    assert scaler is not None

    assert hasattr(
        scaler,
        "transform"
    )


# TEST MODEL PREDICTION

def test_model_prediction():

    result = predict_transaction(
        SAMPLE_TRANSACTION
    )

    assert result is not None

    assert "prediction" in result

    assert "fraud_probability" in result

    assert "is_fraud" in result


# TEST PREDICTION VALUE

def test_prediction_value():

    result = predict_transaction(
        SAMPLE_TRANSACTION
    )

    assert result["prediction"] in [
        0,
        1
    ]


# TEST FRAUD PROBABILITY

def test_fraud_probability():

    result = predict_transaction(
        SAMPLE_TRANSACTION
    )

    probability = result[
        "fraud_probability"
    ]

    assert 0 <= probability <= 1


# TEST IS_FRAUD TYPE

def test_is_fraud_type():

    result = predict_transaction(
        SAMPLE_TRANSACTION
    )

    assert isinstance(
        result["is_fraud"],
        bool
    )


# TEST THRESHOLD

def test_threshold():

    result = predict_transaction(
        SAMPLE_TRANSACTION
    )

    assert "threshold" in result

    assert result["threshold"] == 0.5


# TEST MODEL SOURCE

def test_model_source():

    result = predict_transaction(
        SAMPLE_TRANSACTION
    )

    assert "model_source" in result

    assert result["model_source"] in [
        "mlflow",
        "local"
    ]


# TEST MODEL VERSION

def test_model_version():

    result = predict_transaction(
        SAMPLE_TRANSACTION
    )

    assert "model_version" in result