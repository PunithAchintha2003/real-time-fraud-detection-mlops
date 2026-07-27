from fastapi.testclient import TestClient

from api.main import app


# TEST CLIENT

# Using TestClient as a context manager ensures that
# FastAPI lifespan startup events are executed.
with TestClient(app) as client:

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

        assert data["model_source"] in [
            "mlflow",
            "local"
        ]

        assert data["model_version"] is not None


    # TEST MODEL INFO ENDPOINT

    def test_model_info_endpoint():

        response = client.get(
            "/model-info"
        )

        assert response.status_code == 200

        data = response.json()

        assert (
            data["registered_model"]
            == "FraudDetectionModel"
        )

        assert (
            data["model_alias"]
            == "@champion"
        )

        assert data["model_version"] is not None

        assert data["model_type"] in [
            "RandomForestClassifier",
            "LogisticRegression"
        ]

        assert data["features"] == 30

        assert (
            data["fraud_threshold"]
            == 0.5
        )

        assert data["model_source"] in [
            "mlflow",
            "local"
        ]

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

        assert "threshold" in data

        assert "result" in data

        assert "model_source" in data

        assert "model_version" in data


    # TEST PREDICTION VALUE

    def test_prediction_value():

        response = client.post(
            "/predict",
            json=SAMPLE_TRANSACTION
        )

        assert response.status_code == 200

        data = response.json()

        assert data["prediction"] in [
            0,
            1
        ]


    # TEST IS FRAUD VALUE

    def test_is_fraud_value():

        response = client.post(
            "/predict",
            json=SAMPLE_TRANSACTION
        )

        assert response.status_code == 200

        data = response.json()

        assert data["is_fraud"] in [
            True,
            False
        ]

        assert (
            data["is_fraud"]
            == (
                data["prediction"] == 1
            )
        )


    # TEST FRAUD PROBABILITY

    def test_fraud_probability():

        response = client.post(
            "/predict",
            json=SAMPLE_TRANSACTION
        )

        assert response.status_code == 200

        data = response.json()

        probability = (
            data["fraud_probability"]
        )

        assert isinstance(
            probability,
            float
        )

        assert 0 <= probability <= 1


    # TEST FRAUD THRESHOLD

    def test_fraud_threshold():

        response = client.post(
            "/predict",
            json=SAMPLE_TRANSACTION
        )

        assert response.status_code == 200

        data = response.json()

        assert (
            data["threshold"]
            == 0.5
        )


    # TEST RESULT LABEL

    def test_result_label():

        response = client.post(
            "/predict",
            json=SAMPLE_TRANSACTION
        )

        assert response.status_code == 200

        data = response.json()

        assert data["result"] in [
            "Fraudulent",
            "Legitimate"
        ]

        if data["is_fraud"]:

            assert (
                data["result"]
                == "Fraudulent"
            )

        else:

            assert (
                data["result"]
                == "Legitimate"
            )


    # TEST MODEL SOURCE

    def test_model_source():

        response = client.post(
            "/predict",
            json=SAMPLE_TRANSACTION
        )

        assert response.status_code == 200

        data = response.json()

        assert data["model_source"] in [
            "mlflow",
            "local"
        ]


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

        # Missing V1 to V28 features
        assert response.status_code == 422


    # TEST NEGATIVE AMOUNT

    def test_negative_amount():

        invalid_transaction = (
            SAMPLE_TRANSACTION.copy()
        )

        invalid_transaction[
            "Amount"
        ] = -100

        response = client.post(
            "/predict",
            json=invalid_transaction
        )

        # Negative amount is invalid
        assert response.status_code == 422


    # TEST INVALID TIME TYPE

    def test_invalid_time_type():

        invalid_transaction = (
            SAMPLE_TRANSACTION.copy()
        )

        invalid_transaction[
            "Time"
        ] = "invalid"

        response = client.post(
            "/predict",
            json=invalid_transaction
        )

        assert response.status_code == 422


    # TEST INVALID FEATURE TYPE

    def test_invalid_feature_type():

        invalid_transaction = (
            SAMPLE_TRANSACTION.copy()
        )

        invalid_transaction[
            "V1"
        ] = "invalid"

        response = client.post(
            "/predict",
            json=invalid_transaction
        )

        assert response.status_code == 422


    # TEST ZERO AMOUNT

    def test_zero_amount():

        transaction = (
            SAMPLE_TRANSACTION.copy()
        )

        transaction[
            "Amount"
        ] = 0

        response = client.post(
            "/predict",
            json=transaction
        )

        # Zero is a valid amount
        assert response.status_code == 200

        data = response.json()

        assert "prediction" in data

        assert "fraud_probability" in data

        assert "is_fraud" in data