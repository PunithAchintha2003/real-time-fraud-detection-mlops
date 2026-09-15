# Real-Time Fraud Detection MLOps Platform

<p align="center">

![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![NestJS](https://img.shields.io/badge/NestJS-E0234E?style=for-the-badge&logo=nestjs&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![MLflow](https://img.shields.io/badge/MLflow-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Azure](https://img.shields.io/badge/Microsoft_Azure-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)

</p>

A production-oriented, full-stack **MLOps platform for real-time fraud detection**, designed to demonstrate an end-to-end machine-learning production workflow.

The platform combines a **Next.js frontend**, **NestJS backend**, **PostgreSQL**, **FastAPI machine-learning inference**, **MLflow experiment tracking and model registry**, **automated model retraining**, **Docker**, **Kubernetes**, **Prometheus/Grafana observability**, **GitHub Actions CI/CD**, and **Microsoft Azure cloud deployment**.

The project demonstrates how a machine-learning application can progress from **model development and evaluation** to **model registration, governed promotion, authenticated inference, persistence, observability, automated retraining, containerization, orchestration, CI/CD, and cloud deployment**.

> **Note:** The fraud detection models in this repository use synthetic/demo data for engineering and MLOps demonstration purposes. Model performance on synthetic data should not be interpreted as real-world fraud detection accuracy.

---

# Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
  - [Application](#application)
  - [Machine Learning](#machine-learning)
  - [MLOps / DevOps](#mlops--devops)
- [Architecture](#architecture)
  - [Logical Architecture](#logical-architecture)
  - [Production Cloud Architecture](#production-cloud-architecture)
  - [Request and Prediction Flow](#request-and-prediction-flow)
  - [Machine Learning / MLOps Lifecycle](#machine-learning--mlops-lifecycle)
- [Automated Retraining](#automated-retraining)
- [Machine Learning Services](#machine-learning-services)
- [Full-Stack API](#full-stack-api)
  - [Authentication](#authentication)
  - [Transactions](#transactions)
- [Repository Structure](#repository-structure)
- [Technology Stack](#technology-stack)
  - [Frontend](#frontend)
  - [Backend](#backend)
  - [Machine Learning](#machine-learning-1)
  - [Containerization](#containerization)
  - [Orchestration](#orchestration)
  - [CI/CD](#cicd)
  - [Cloud](#cloud)
  - [Observability](#observability)
- [Local Docker Environment](#local-docker-environment)
- [Running the Local Full Stack](#running-the-local-full-stack)
- [Local Application URLs](#local-application-urls)
- [Health Checks](#health-checks)
- [Observability](#observability-1)
  - [Prometheus Targets](#prometheus-targets)
  - [Backend Metrics](#backend-metrics)
  - [Machine Learning Metrics](#machine-learning-metrics)
- [Kubernetes Deployment](#kubernetes-deployment)
- [GitHub Actions CI/CD](#github-actions-cicd)
- [Testing](#testing)
- [Local Development](#local-development)
  - [Backend](#backend-1)
  - [Frontend](#frontend-1)
  - [ML Service](#ml-service)
- [Environment Configuration](#environment-configuration)
  - [Backend Environment Variables](#backend-environment-variables)
  - [Frontend Environment Variables](#frontend-environment-variables)
  - [ML Service Environment Variables](#ml-service-environment-variables)
- [Azure Cloud Deployment](#azure-cloud-deployment)
  - [Azure Architecture](#azure-architecture)
  - [Container Image Flow](#container-image-flow)
- [Azure Service Responsibilities](#azure-service-responsibilities)
- [Security](#security)
  - [Application Security](#application-security)
  - [Azure Security](#azure-security)
  - [Production Hardening Considerations](#production-hardening-considerations)
- [Model Registry](#model-registry)
- [Model Promotion Strategy](#model-promotion-strategy)
- [Engineering Highlights](#engineering-highlights)
- [Project Limitations](#project-limitations)
- [Current Project Status](#current-project-status)
- [Author](#author)

---

# Project Overview

The platform provides a complete real-time fraud detection workflow:

1. Users register and authenticate through the web application.
2. Authenticated users submit transaction information.
3. The NestJS backend validates and stores transaction data.
4. The backend acts as a secure gateway to the FastAPI machine-learning service.
5. The ML service performs feature engineering and model inference.
6. The prediction result is returned to the backend and persisted in PostgreSQL.
7. Users can review historical transactions and prediction results.
8. MLflow manages model experiments, registered models, versions, and champion aliases.
9. Automated retraining evaluates candidate models against the current champion model.
10. Prometheus and Grafana provide application and machine-learning observability.
11. Docker and Kubernetes provide local and containerized deployment paths.
12. GitHub Actions provides automated CI/CD validation and container image publishing.
13. Azure Container Apps provides a cloud deployment architecture for the platform.

---

# Key Features

## Application

- User registration and authentication
- JWT access-token authentication
- Refresh-token authentication using secure HTTP-only cookies
- Protected API endpoints
- Real-time transaction fraud-check workflow
- Transaction history
- Fraud probability and risk-level results
- Next.js web dashboard
- NestJS backend API gateway
- Persistent transaction and prediction history

## Machine Learning

- Fraud detection model training
- Business fraud model training
- Feature engineering
- Model evaluation
- MLflow experiment tracking
- MLflow Model Registry
- Champion model aliases
- FastAPI inference API
- ML model hot reload
- Last-known-good model fallback
- Automated model retraining
- Candidate-vs-champion quality gate

## MLOps / DevOps

- Dockerized services
- Full-stack Docker Compose environment
- Kubernetes manifests
- Kubernetes Jobs
- Kubernetes CronJobs for automated retraining
- GitHub Actions CI
- Docker image build validation
- Docker Hub image publishing
- Azure Container Registry
- Azure Container Apps deployment
- Azure PostgreSQL Flexible Server
- Azure Log Analytics
- Prometheus monitoring
- Grafana dashboards
- ML-specific monitoring metrics
- Feature drift monitoring
- Production-oriented model promotion workflow

---

# Architecture

## Logical Architecture

```text
User
  │
  ▼
Next.js Frontend
  │
  │ HTTPS / JWT
  ▼
NestJS Backend
  │
  ├──► PostgreSQL
  │       ├── users
  │       ├── transactions
  │       └── prediction history
  │
  └──► FastAPI ML Service
          │
          └──► MLflow
                  ├── Experiment Tracking
                  ├── Model Registry
                  └── Champion Model
                          │
                          ▼
                     Fraud Prediction
                          │
                          ▼
                  NestJS Backend
                          │
                          ▼
                  Next.js Dashboard
```

## Production Cloud Architecture

```text
GitHub Repository
  │
  ▼
GitHub Actions
  │
  │ Build / Test / Publish
  ▼
Azure Container Registry
  │
  ▼
Azure Container Apps Environment
  │
  ├──► Frontend Container App
  │       │
  │       └──► Backend Container App
  │
  ├──► Backend Container App
  │       ├──► Azure PostgreSQL Flexible Server
  │       └──► ML Service Container App
  │                │
  │                └──► MLflow Container App
  │                         │
  │                         └──► Azure PostgreSQL Flexible Server
  │
  ├──► ML Service Container App
  │
  └──► MLflow Container App
          │
          ▼
    Azure Log Analytics

Frontend Container App
          │
          ▼
Backend Container App
          │
          ▼
ML Service Container App
          │
          ▼
MLflow Champion Model
```

## Request and Prediction Flow

```text
User
  │
  ▼
Next.js Frontend
  │
  │ JWT-authenticated request
  ▼
NestJS Backend
  │
  ├──► PostgreSQL
  │       └── users / transactions / prediction history
  │
  └──► FastAPI ML Service
          │
          └──► MLflow Champion Model
                  │
                  ▼
             Fraud Prediction
                  │
                  ▼
          NestJS Backend
                  │
                  ▼
          Next.js Dashboard
```

## Machine Learning / MLOps Lifecycle

```text
Training Data
  │
  ▼
Preprocessing
  │
  ▼
Model Training
  │
  ▼
Model Evaluation
  │
  ├──────────────► Quality Gate
  │                    │
  │             ┌──────┴──────┐
  │             │             │
  │           Pass            Fail
  │             │             │
  │             ▼             ▼
  │      MLflow Registry   Automated
  │             │          Retraining
  │             ▼             │
  │       Champion Alias     │
  │             │             │
  │             ▼             │
  │      FastAPI Inference    │
  │             │             │
  │             ▼             │
  │         Monitoring        │
  │             │             │
  │             ▼             │
  │      Automated Retraining─┘
  │
  └──────────────► MLflow Tracking
                         │
                         ▼
                 MLflow Model Registry
```

---

# Automated Retraining

The business fraud model includes an automated retraining workflow.

A newly trained candidate model is evaluated against the current champion model using:

- Precision
- Recall
- F1 score
- ROC-AUC

The production quality gate requires:

```text
candidate F1 > champion F1
AND
candidate ROC-AUC >= champion ROC-AUC
```

Only candidates that satisfy the quality gate are promoted to the `champion` alias.

The production inference service uses the `champion` alias instead of hard-coding a specific model version. This allows model versions to be promoted without requiring application code changes.

Kubernetes automation is represented by:

```text
infrastructure/kubernetes/retraining-cronjob.yaml
```

The retraining workflow also preserves the last-known-good model if a newly loaded model fails validation or cannot be loaded successfully at runtime.

> **Note:** The fraud models in this project use synthetic/demo training data for MLOps demonstration purposes. High evaluation scores on synthetic data should not be interpreted as real-world fraud detection performance.

---

# Machine Learning Services

The ML service is implemented using:

- **Python**
- **FastAPI**
- **scikit-learn**
- **pandas**
- **NumPy**
- **MLflow**
- **joblib**
- **Prometheus client instrumentation**

The service exposes the following endpoints:

```text
GET  /health
GET  /metrics
POST /predict
POST /predict/business
```

The exact API contract is defined by the implementation under:

```text
apps/ml-service/
```

The ML service loads the active champion model from MLflow and exposes prediction metadata such as:

- Prediction
- Fraud probability
- Decision threshold
- Result
- Risk level
- Model type
- Model version
- Features used

---

# Full-Stack API

## Authentication

```text
POST /auth/register
POST /auth/login
POST /auth/refresh
POST /auth/logout
GET  /auth/me
```

Protected endpoints require JWT authentication.

The authentication layer supports access-token authentication together with refresh-token handling through secure HTTP-only cookies.

## Transactions

```text
POST /transactions/check
GET  /transactions
GET  /transactions/:id
```

The backend is responsible for:

- Authentication
- Request validation
- Transaction persistence
- Communication with the ML service
- Prediction persistence
- Transaction history retrieval

---

# Repository Structure

```text
real-time-fraud-detection-mlops/
│
├── apps/
│   ├── frontend/
│   │   └── Next.js application
│   │
│   ├── backend/
│   │   └── NestJS API
│   │
│   └── ml-service/
│       └── FastAPI ML inference service
│
├── infrastructure/
│   ├── docker/
│   │   ├── Dockerfiles
│   │   ├── docker-compose.yml
│   │   ├── docker-compose.monitoring.yml
│   │   └── MLflow / registration utilities
│   │
│   ├── kubernetes/
│   │   ├── frontend.yaml
│   │   ├── backend.yaml
│   │   ├── ml-service.yaml
│   │   ├── mlflow.yaml
│   │   ├── postgres.yaml
│   │   ├── trainer-job.yaml
│   │   ├── retraining-cronjob.yaml
│   │   ├── prometheus.yaml
│   │   ├── grafana.yaml
│   │   └── grafana-dashboard.yaml
│   │
│   └── monitoring/
│       ├── prometheus/
│       ├── grafana/
│       └── README.md
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── package.json
├── package-lock.json
├── LICENSE
└── README.md
```

---

# Technology Stack

## Frontend

- **Next.js**
- **React**
- **TypeScript**
- **Tailwind CSS**

## Backend

- **NestJS**
- **TypeScript**
- **PostgreSQL**
- **Prisma ORM**
- **Passport.js**
- **JWT**
- **bcrypt**

## Machine Learning

- **Python**
- **FastAPI**
- **scikit-learn**
- **pandas**
- **NumPy**
- **joblib**
- **MLflow**

## Containerization

- **Docker**
- **Docker Compose**

## Orchestration

- **Kubernetes**
- **Kubernetes Jobs**
- **Kubernetes CronJobs**

## CI/CD

- **GitHub Actions**
- **Docker Build**
- **Docker Hub**
- **Azure Container Registry**

## Cloud

- **Azure Container Apps**
- **Azure Container Apps Environment**
- **Azure PostgreSQL Flexible Server**
- **Azure Container Registry**
- **Azure Log Analytics**
- **Managed Identity for container image pulling**

## Observability

- **Prometheus**
- **Grafana**
- **Azure Log Analytics**

---

# Local Docker Environment

The full-stack Docker Compose environment includes the following services:

| Service | Purpose | Port |
|---|---|---:|
| Frontend | Next.js web application | `3000` |
| Backend | NestJS API | `4000` |
| ML API | FastAPI inference service | `8000` |
| MLflow | ML experiment tracking and model registry | `5001` |
| PostgreSQL | Application database | `55432` |

The local monitoring stack additionally includes:

| Service | Purpose | Port |
|---|---|---:|
| Prometheus | Metrics collection | `9090` |
| Grafana | Metrics visualization and dashboards | `3001` |

---

# Running the Local Full Stack

From the repository root, start the full application stack:

```bash
docker compose -f infrastructure/docker/docker-compose.yml up -d --build
```

Start the local monitoring stack:

```bash
docker compose -f infrastructure/docker/docker-compose.monitoring.yml up -d
```

Check running services:

```bash
docker ps | grep fraud-detection
```

Expected application services include:

```text
fraud-detection-postgres
fraud-detection-mlflow
fraud-detection-api
fraud-detection-backend
fraud-detection-frontend
```

Expected monitoring services include:

```text
fraud-detection-prometheus
fraud-detection-grafana
```

---

# Local Application URLs

| Application | URL |
|---|---|
| Frontend | [http://localhost:3000](http://localhost:3000) |
| Backend API | [http://localhost:4000](http://localhost:4000) |
| ML API | [http://localhost:8000](http://localhost:8000) |
| MLflow | [http://localhost:5001](http://localhost:5001) |
| Prometheus | [http://localhost:9090](http://localhost:9090) |
| Grafana | [http://localhost:3001](http://localhost:3001) |

---

# Health Checks

## Backend

```bash
curl http://localhost:4000
```

## ML Service

```bash
curl http://localhost:8000/health | python -m json.tool
```

## ML Metrics

```bash
curl http://localhost:8000/metrics
```

## Backend Metrics

```bash
curl http://localhost:4000/metrics
```

## Frontend

```bash
curl -I http://localhost:3000
```

## MLflow

```bash
curl http://localhost:5001/health
```

---

# Observability

The local observability stack uses **Prometheus** for metrics collection and **Grafana** for metrics visualization and dashboarding.

## Prometheus Targets

Prometheus scrapes the following targets:

```text
fraud-backend
fraud-ml-service
prometheus
```

Expected target state:

```text
fraud-backend     UP
fraud-ml-service  UP
prometheus        UP
```

## Backend Metrics

Examples of backend application metrics include:

```text
fraud_backend_http_requests_total
fraud_backend_http_request_duration_seconds
fraud_backend_app_info
```

## Machine Learning Metrics

Examples of ML-specific metrics include:

```text
ml_business_predictions_total
ml_business_fraud_rate
ml_business_legitimate_rate
ml_business_prediction_window_size
ml_business_amount_distribution
ml_business_probability_distribution
ml_business_total_risk_score_distribution
ml_business_feature_value
ml_business_feature_drift_score
ml_business_drift_alerts_total
```

These metrics support:

- Request monitoring
- Prediction volume monitoring
- Fraud-rate monitoring
- Risk distribution monitoring
- Probability distribution monitoring
- Feature-drift monitoring
- Drift alert tracking

Grafana dashboards are provisioned from:

```text
infrastructure/monitoring/grafana/
```

Additional monitoring configuration and operational details are available in:

```text
infrastructure/monitoring/README.md
```

---

# Kubernetes Deployment

Kubernetes manifests are stored in:

```text
infrastructure/kubernetes/
```

The Kubernetes environment includes resources for:

- Namespace
- PostgreSQL
- MLflow
- ML service
- Backend
- Frontend
- Backend database migrations
- Model trainer
- Automated retraining
- Prometheus
- Grafana

Core manifests include:

```text
namespace.yaml
postgres.yaml
mlflow.yaml
ml-service.yaml
backend.yaml
frontend.yaml
backend-migrate-job.yaml
trainer-job.yaml
retraining-cronjob.yaml
prometheus.yaml
grafana.yaml
grafana-dashboard.yaml
```

The Kubernetes deployment path is intended for local container-orchestration demonstrations and platform engineering practice.

---

# GitHub Actions CI/CD

The project uses **GitHub Actions** for automated validation and continuous integration.

The main workflow is:

```text
.github/workflows/ci.yml
```

The CI pipeline validates the following components.

## ML Service

- Python environment setup
- Dependency installation
- Import validation
- CI model artifact creation
- Business model training
- `pytest` test suite execution

## Backend

- npm dependency installation
- Prisma Client generation
- Linting
- Production build

## Frontend

- npm dependency installation
- Production build

## Docker

- Docker Compose configuration validation
- ML service image build
- Backend image build
- Frontend image build

## Docker Hub

When the configured workflow runs on the `main` branch, the ML service image can be published to Docker Hub using GitHub repository secrets.

---

# Testing

The ML service includes automated tests using **pytest**.

Run the ML test suite locally with:

```bash
pytest -q apps/ml-service/tests
```

The test suite validates model and API behavior across the ML service.

The same ML test suite is executed automatically as part of the GitHub Actions CI pipeline.

---

# Local Development

## Backend

```bash
cd apps/backend
npm install
cp .env.example .env
npm run prisma:generate
npm run start:dev
```

## Frontend

```bash
cd apps/frontend
npm install
cp .env.example .env.local
npm run dev
```

## ML Service

```bash
cd apps/ml-service
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

---

# Environment Configuration

Local environment variables should be stored in `.env` and `.env.local` files.

Production credentials and secrets must never be committed to source control.

## Backend Environment Variables

Example:

```env
DATABASE_URL="postgresql://..."
JWT_SECRET="change_this_secret"
JWT_EXPIRES_IN="15m"
JWT_REFRESH_SECRET="change_this_refresh_secret"
JWT_REFRESH_EXPIRES_IN="7d"
PORT=4000
ML_SERVICE_URL="http://localhost:8000"
```

## Frontend Environment Variables

Example:

```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:4000
```

## ML Service Environment Variables

Example:

```env
MLFLOW_TRACKING_URI=http://localhost:5001
```

Actual production credentials and secrets are supplied through deployment configuration and secret-management mechanisms rather than committed to Git.

---

# Azure Cloud Deployment

The project includes a cloud deployment architecture built on **Microsoft Azure Container Apps**.

The architecture separates the platform into independently deployable containerized services while providing managed database, container registry, logging, storage, and identity capabilities.

## Azure Architecture

```text
Azure Resource Group
  │
  ├──► Azure Container Apps Environment
  │       ├──► Frontend Container App
  │       ├──► Backend Container App
  │       ├──► ML Service Container App
  │       └──► MLflow Container App
  │
  ├──► Azure Container Registry
  │
  ├──► Azure PostgreSQL Flexible Server
  │
  ├──► Azure Log Analytics
  │
  ├──► Azure Storage
  │       └──► MLflow Artifacts
  │
  └──► Managed Identity
          └──► Azure Container Registry Pull Permission
```

## Container Image Flow

```text
GitHub Repository
       │
       ▼
GitHub Actions
       │
       │ Build / Test / Publish
       ▼
Azure Container Registry
       │
       │ Container Images
       ▼
Azure Container Apps
       │
       ├──► Frontend
       ├──► Backend
       ├──► ML Service
       └──► MLflow
```

The cloud deployment separates application services into independently deployable containers, allowing each service to be built, deployed, scaled, and maintained independently.

---

# Azure Service Responsibilities

## Frontend Container App

Hosts the production **Next.js** application and provides the user-facing web interface.

## Backend Container App

Provides:

- Authentication and authorization
- Transaction APIs
- PostgreSQL integration
- ML service gateway functionality
- Transaction persistence and history

## ML Service Container App

Provides:

- FastAPI inference endpoints
- Champion-model loading
- Fraud prediction
- Health-check endpoint
- Prometheus-compatible metrics

## MLflow Container App

Provides:

- Experiment tracking
- Model registry
- Champion model aliases
- Model artifact management

## Azure PostgreSQL Flexible Server

Provides the production relational database required by the backend and MLflow components.

## Azure Container Registry

Stores the container images consumed by Azure Container Apps.

## Azure Log Analytics

Collects application and system logs from the Azure Container Apps environment for operational monitoring and troubleshooting.

## Azure Storage

Provides persistent storage for MLflow model artifacts and related files.

## Managed Identity

Provides identity-based access from Azure Container Apps to Azure Container Registry without embedding registry credentials directly into the application configuration.

---

# Security

The application implements multiple security controls across authentication, credentials, API access, configuration, and cloud infrastructure.

## Application Security

- JWT-based authentication
- Short-lived access tokens
- Refresh-token authentication flow
- Secure HTTP-only refresh-token cookies
- Password hashing with `bcrypt`
- Protected backend routes
- Authenticated transaction operations
- Environment-based configuration
- Git-ignored environment files

## Azure Security

- Managed Identity for container image access
- Container Registry authentication without hard-coded registry credentials
- Environment-based secret injection
- Least-privilege access considerations

## Production Hardening Considerations

Additional production hardening should include:

- Secure secret management
- Strict CORS configuration
- API rate limiting
- Database backup and recovery policies
- Network access restrictions
- Least-privilege identity assignments
- TLS/HTTPS enforcement
- Audit logging
- Production monitoring and alerting

---

# Model Registry

The platform uses **MLflow Registered Models** and model aliases to manage deployed model versions.

Primary registered models include:

```text
FraudDetectionModel
BusinessFraudDetectionModel
```

The deployed inference service loads the active model through the `champion` alias rather than relying exclusively on a hard-coded model version.

This allows a newly validated model to be promoted into production without requiring changes to the inference application code for every model version.

---

# Model Promotion Strategy

The automated model promotion workflow follows a candidate-versus-champion evaluation process:

```text
Candidate Model
      │
      ▼
   Evaluate
      │
      ├──► F1 improvement?
      │
      └──► ROC-AUC maintained?
             │
        ┌────┴────┐
        │         │
       YES        NO
        │         │
        ▼         ▼
   Promote      Reject
   to Champion  Candidate
        │
        ▼
Production Inference
```

The quality gate requires:

```text
candidate F1 > champion F1
AND
candidate ROC-AUC >= champion ROC-AUC
```

This provides a simple, reproducible promotion strategy for automated retraining while preventing lower-quality candidates from replacing the current champion model.

---

# Engineering Highlights

This project demonstrates practical engineering experience across software development, machine learning, MLOps, DevOps, platform engineering, and observability.

```text
Software Engineering
        │
        ├──► Next.js / React
        ├──► NestJS / TypeScript
        ├──► PostgreSQL / Prisma
        └──► API Design

Machine Learning
        │
        ├──► Feature Engineering
        ├──► Model Training
        ├──► Model Evaluation
        └──► Inference Serving

MLOps
        │
        ├──► MLflow
        ├──► Model Registry
        ├──► Champion Aliases
        ├──► Automated Retraining
        └──► Quality Gates

DevOps / Platform Engineering
        │
        ├──► Docker
        ├──► Kubernetes
        ├──► GitHub Actions
        ├──► Container Registry
        └──► Azure Container Apps

Observability
        │
        ├──► Prometheus
        ├──► Grafana
        ├──► ML Metrics
        ├──► Drift Metrics
        └──► Azure Log Analytics
```

---

# Project Limitations

This project is an **engineering and MLOps demonstration platform** designed to demonstrate an end-to-end machine-learning production workflow.

The fraud detection models use **synthetic/demo data** rather than a production financial dataset. Therefore:

- Model evaluation metrics demonstrate the training, evaluation, deployment, and monitoring pipeline.
- Performance on synthetic data does not represent real-world fraud detection accuracy.
- A real deployment would require domain-specific, representative financial transaction data.
- Production deployment would require additional compliance, security, privacy, governance, and operational controls.
- Real-world fraud detection systems would require continuous monitoring, retraining, validation, and domain-specific risk management.

> **Important:** This project should not be used as a production financial fraud detection system without appropriate domain validation, security review, compliance assessment, and operational controls.

---

# Current Project Status

The complete development roadmap has been implemented through **Phase 31**:

| Phase | Implementation | Status |
|---:|---|:---:|
| 01 | Project Setup | ✅ |
| 02 | Data Preprocessing | ✅ |
| 03 | Model Training | ✅ |
| 04 | Model Evaluation | ✅ |
| 05 | MLflow Tracking | ✅ |
| 06 | MLflow Model Registry | ✅ |
| 07 | Champion Model Alias | ✅ |
| 08 | FastAPI Inference API | ✅ |
| 09 | Product-style Fraud API | ✅ |
| 10 | Frontend UI + Fraud Form | ✅ |
| 11 | Pytest / ML & API Testing | ✅ |
| 12 | Docker | ✅ |
| 13 | Docker Compose + MLflow | ✅ |
| 14 | GitHub Actions CI | ✅ |
| 15 | Docker Hub CI/CD | ✅ |
| 16 | Kubernetes Local Deployment | ✅ |
| 17 | Monorepo Restructure | ✅ |
| 18 | NestJS Backend + PostgreSQL + Prisma | ✅ |
| 19 | Register / Login + Dashboard UI | ✅ |
| 20 | Backend Prediction Gateway | ✅ |
| 21 | Transaction History UI | ✅ |
| 22 | Backend + Frontend Cleanup | ✅ |
| 23 | Full-stack Docker Compose Update | ✅ |
| 24 | Full-stack GitHub Actions CI/CD Update | ✅ |
| 25 | Kubernetes Full-stack Update | ✅ |
| 26 | Observability v2 | ✅ |
| 27 | ML Monitoring v2 | ✅ |
| 28 | Authentication Security + UX Upgrade | ✅ |
| 29 | Automated Retraining | ✅ |
| 30 | Azure / Cloud Deployment | ✅ |
| 31 | Production README + Architecture | ✅ |

---

# Author

## Punith Achintha

**BSc (Hons) Software Engineering**

**Full-Stack Developer | MLOps | AI Infrastructure**

### GitHub

[github.com/PunithAchintha2003](https://github.com/PunithAchintha2003)

### LinkedIn

[linkedin.com/in/punith-hirimbura](https://www.linkedin.com/in/punith-hirimbura)

### Portfolio

[punith-achintha-portfolio.vercel.app](https://punith-achintha-portfolio.vercel.app)

---

<p align="center">
  <sub>Built as an end-to-end software engineering, machine learning, MLOps, DevOps, and cloud engineering portfolio project.</sub>
</p>