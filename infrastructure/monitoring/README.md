# Observability

This directory contains monitoring and observability notes for the Real-Time Fraud Detection MLOps platform.

## Kubernetes Observability Stack

The Kubernetes observability stack includes:

- Prometheus for metrics collection
- Grafana for visualization
- Backend `/metrics` endpoint using `prom-client`
- ML service `/metrics` endpoint using Prometheus-compatible metrics
- Provisioned Grafana Prometheus datasource
- Provisioned Fraud Detection Observability dashboard

## Kubernetes Manifests

Monitoring-related Kubernetes manifests are stored in:

- `infrastructure/kubernetes/prometheus.yaml`
- `infrastructure/kubernetes/grafana.yaml`
- `infrastructure/kubernetes/grafana-dashboard.yaml`

## Prometheus Targets

Prometheus scrapes:

- `prometheus`
- `fraud-backend`
- `fraud-ml-service`

Expected target status:

- `prometheus` UP
- `fraud-backend` UP
- `fraud-ml-service` UP

## Local Port Forwarding

Prometheus:

    kubectl port-forward -n fraud-detection svc/prometheus-service 30090:9090

Grafana:

    kubectl port-forward -n fraud-detection svc/grafana-service 33300:3000

Open:

- Prometheus: `http://localhost:30090`
- Grafana: `http://localhost:33300`

Grafana login:

- Username: `admin`
- Password: `admin`

## Useful Prometheus Queries

Backend request rate:

    sum by (method, route, status_code) (rate(fraud_backend_http_requests_total[5m]))

Backend p95 latency:

    histogram_quantile(0.95, sum by (le, route) (rate(fraud_backend_http_request_duration_seconds_bucket[5m])))

Backend memory:

    fraud_backend_process_resident_memory_bytes

ML service memory:

    process_resident_memory_bytes{job="fraud-ml-service"}

Target availability:

    up

## Grafana Dashboard

Dashboard manifest:

- `infrastructure/kubernetes/grafana-dashboard.yaml`

Dashboard folder:

- `Fraud Detection MLOps`

Dashboard name:

- `Fraud Detection Observability`

## ML Monitoring v2

ML monitoring metrics are exposed by the FastAPI ML service and scraped by Prometheus.

Key metrics:

- `ml_business_predictions_total`
- `ml_business_fraud_rate`
- `ml_business_legitimate_rate`
- `ml_business_prediction_window_size`
- `ml_business_amount_distribution`
- `ml_business_probability_distribution`
- `ml_business_risk_score_distribution`
- `ml_business_feature_drift_score`
- `ml_business_drift_alerts_total`

Useful ML monitoring queries:

    ml_business_prediction_window_size

    ml_business_fraud_rate

    ml_business_legitimate_rate

    sum by (result, risk_level) (rate(ml_business_predictions_total[5m]))

    histogram_quantile(0.95, rate(ml_business_probability_distribution_bucket[5m]))

    histogram_quantile(0.95, rate(ml_business_amount_distribution_bucket[5m]))

    histogram_quantile(0.95, rate(ml_business_risk_score_distribution_bucket[5m]))

    max by (feature) (ml_business_feature_drift_score)

    sum(increase(ml_business_drift_alerts_total[15m]))

The Grafana dashboard includes ML Monitoring v2 panels for prediction volume, fraud rate, legitimate rate, probability distribution, transaction amount distribution, risk score distribution, and feature drift scores.

