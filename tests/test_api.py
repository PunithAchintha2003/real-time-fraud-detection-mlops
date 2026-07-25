from fastapi.testclient import TestClient

from api.main import app

# TEST CLIENT

client = TestClient(app)

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

# TEST HEALTH ENDPOINT

def test_health_endpoint():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"

    assert data["model_loaded"] is True

# TEST MODEL INFO ENDPOINT

def test_model_info_endpoint():

    response = client.get(
        "/model-info"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["model_type"] in [
        "RandomForestClassifier",
        "LogisticRegression"
    ]

    assert data["features"] == 30

    assert data["status"] == "loaded"

# TEST PREDICTION ENDPOINT

def test_prediction_endpoint():

    response = client.post(
        "/predict",
        json=SAMPLE_TRANSACTION
    )

    assert response.status_code == 200

    data = response.json()

    assert "prediction" in data

    assert "is_fraud" in data

    assert "fraud_probability" in data

    assert "result" in data

# TEST PREDICTION VALUE

def test_prediction_value():

    response = client.post(
        "/predict",
        json=SAMPLE_TRANSACTION
    )

    data = response.json()

    assert data["prediction"] in [
        0,
        1
    ]

# TEST FRAUD PROBABILITY

def test_fraud_probability():

    response = client.post(
        "/predict",
        json=SAMPLE_TRANSACTION
    )

    data = response.json()

    assert 0 <= data[
        "fraud_probability"
    ] <= 1

# TEST INVALID INPUT

def test_invalid_input():

    invalid_transaction = {
        "Time": 406,
        "Amount": 149.62
    }

    response = client.post(
        "/predict",
        json=invalid_transaction
    )

    assert response.status_code == 422

# TEST NEGATIVE AMOUNT

def test_negative_amount():

    invalid_transaction = SAMPLE_TRANSACTION.copy()

    invalid_transaction[
        "Amount"
    ] = -100

    response = client.post(
        "/predict",
        json=invalid_transaction
    )

    assert response.status_code == 422