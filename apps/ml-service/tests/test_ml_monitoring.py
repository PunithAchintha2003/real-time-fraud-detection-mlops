from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_business_prediction_ml_monitoring_metrics():
    payload = {
        "amount": 7500,
        "merchant_type": "crypto",
        "location": "unknown",
        "transaction_time": "02:30",
        "payment_method": "crypto",
        "device_type": "unknown",
        "is_international": True,
        "previous_failed_attempts": 5,
    }

    prediction_response = client.post(
        "/predict-business",
        json=payload,
    )

    assert prediction_response.status_code == 200

    metrics_response = client.get("/metrics")

    assert metrics_response.status_code == 200

    body = metrics_response.text

    assert "ml_business_predictions_total" in body
    assert "ml_business_fraud_rate" in body
    assert "ml_business_legitimate_rate" in body
    assert "ml_business_amount_distribution" in body
    assert "ml_business_probability_distribution" in body
    assert "ml_business_total_risk_score_distribution" in body
    assert "ml_business_feature_drift_score" in body
    assert "ml_business_drift_alerts_total" in body
