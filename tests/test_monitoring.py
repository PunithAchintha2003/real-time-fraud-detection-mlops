from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_metrics_endpoint():
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]

    body = response.text

    assert "fraud_api_requests_total" in body
    assert "fraud_api_request_duration_seconds" in body
    assert "fraud_model_loaded" in body
    assert "business_fraud_model_loaded" in body
