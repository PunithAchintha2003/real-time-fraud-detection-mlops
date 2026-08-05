# Real-Time Fraud Detection MLOps Platform

A production-oriented full-stack MLOps platform for real-time fraud detection. The system combines a Next.js frontend, NestJS backend, PostgreSQL authentication database, FastAPI machine learning service, MLflow model registry, Docker-based deployment, and monitoring-ready infrastructure.

## Project Overview

This project demonstrates an end-to-end fraud detection workflow, from machine learning model training and model registry management to authenticated real-time predictions through a full-stack web application.

Users can register, log in, submit transaction details, receive fraud risk predictions, and view prediction history. The backend acts as a secure API gateway between the frontend and the ML service, while the ML service loads registered model artifacts and serves prediction endpoints.

## Key Features

- User registration and login
- JWT-based authentication
- Protected transaction fraud checking
- Real-time fraud prediction using a trained ML model
- Transaction history with prediction results
- PostgreSQL database integration with Prisma
- FastAPI ML inference service
- MLflow model tracking and registry
- Dockerized full-stack environment
- Docker Compose orchestration
- Monitoring-ready infrastructure with Prometheus and Grafana
- Modular monorepo architecture

## Architecture

```mermaid
flowchart LR
    U[User] --> FE[Next.js Frontend]

    FE -->|JWT Auth + API Requests| BE[NestJS Backend API]

    BE -->|User + Transaction Data| DB[(PostgreSQL)]
    BE -->|Prediction Request| ML[FastAPI ML Service]

    ML -->|Load Model| MLFLOW[MLflow Model Registry]
    ML -->|Prediction Response| BE

    BE -->|Prediction + History| FE

    PROM[Prometheus] --> ML
    GRAF[Grafana] --> PROM
```

## System Flow

1. User registers or logs in through the frontend.
2. Backend validates credentials and returns a JWT access token.
3. User submits transaction details from the dashboard.
4. Frontend sends the transaction request to the NestJS backend.
5. Backend validates the JWT and forwards the transaction data to the FastAPI ML service.
6. ML service performs feature engineering and fraud prediction.
7. Backend stores the transaction and prediction result in PostgreSQL.
8. Frontend displays the prediction result and transaction history.

## Tech Stack

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

### Backend

- NestJS
- TypeScript
- PostgreSQL
- Prisma ORM
- JWT Authentication
- Passport.js
- bcrypt

### Machine Learning Service

- Python
- FastAPI
- Scikit-learn
- Pandas
- NumPy
- MLflow

### DevOps / MLOps

- Docker
- Docker Compose
- GitHub Actions
- MLflow Tracking Server
- Prometheus
- Grafana
- Kubernetes-ready infrastructure

## Monorepo Structure

```text
real-time-fraud-detection-mlops/
├── apps/
│   ├── frontend/          # Next.js frontend application
│   ├── backend/           # NestJS backend API and gateway
│   └── ml-service/        # FastAPI ML inference service
│
├── infrastructure/
│   ├── docker/            # Dockerfiles and Docker Compose files
│   ├── kubernetes/        # Kubernetes manifests
│   └── monitoring/        # Prometheus and Grafana configuration
│
├── .github/
│   └── workflows/         # GitHub Actions CI/CD workflows
│
├── README.md
├── package.json
└── .gitignore
```

## Dockerized Services

The full-stack Docker Compose setup runs the following services:

| Service | Description | Port |
|---|---|---|
| Frontend | Next.js web application | 3000 |
| Backend | NestJS API gateway and auth service | 4000 |
| ML Service | FastAPI fraud prediction service | 8000 |
| MLflow | Model tracking and registry server | 5001 |
| PostgreSQL | Authentication and transaction database | 55432 |

## Running the Full Stack with Docker Compose

From the project root:

```bash
docker compose -f infrastructure/docker/docker-compose.yml up -d --build
```

Check running containers:

```bash
docker ps | grep fraud-detection
```

Expected running services:

```text
fraud-detection-postgres
fraud-detection-mlflow
fraud-detection-api
fraud-detection-backend
fraud-detection-frontend
```

The trainer and backend migration containers may exit after completing their tasks. This is expected behavior.

## Application URLs

| Application | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:4000 |
| FastAPI ML Service | http://localhost:8000 |
| MLflow UI | http://localhost:5001 |

## Health Checks

Backend:

```bash
curl http://localhost:4000
```

ML service:

```bash
curl http://localhost:8000/health | python -m json.tool
```

Frontend:

```bash
curl -I http://localhost:3000
```

## Authentication Endpoints

```http
POST /auth/register
POST /auth/login
GET  /auth/me
```

## Transaction Endpoints

```http
POST /transactions/check
GET  /transactions
GET  /transactions/:id
```

## Example Prediction Request

```bash
curl -X POST http://localhost:4000/transactions/check \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d '{
    "amount": 2500,
    "merchant_type": "electronics",
    "location": "Colombo",
    "transaction_time": "14:30",
    "payment_method": "card",
    "device_type": "mobile",
    "is_international": false,
    "previous_failed_attempts": 0
  }'
```

Example response:

```json
{
  "transaction_id": "example-transaction-id",
  "prediction_id": "example-prediction-id",
  "prediction": 0,
  "is_fraud": false,
  "fraud_probability": 0.44639,
  "threshold": 0.5,
  "result": "Legitimate",
  "risk_level": "Low Risk",
  "model_type": "RandomForestClassifier",
  "model_version": "business-v1",
  "features_used": 13
}
```

## Local Development

### Backend

```bash
cd apps/backend
npm install
cp .env.example .env
npm run prisma:generate
npm run start:dev
```

### Frontend

```bash
cd apps/frontend
npm install
cp .env.example .env.local
npm run dev
```

### ML Service

```bash
cd apps/ml-service
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

## Environment Variables

### Backend

```env
DATABASE_URL="postgresql://fraud_user:fraud_password@localhost:55432/fraud_auth_db?schema=public"
JWT_SECRET="change_this_secret_in_production"
JWT_EXPIRES_IN="1d"
PORT=4000
ML_SERVICE_URL="http://localhost:8000"
```

### Frontend

```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:4000
```

Real `.env` files are ignored by Git. Only `.env.example` files should be committed.

## Machine Learning Workflow

The ML workflow includes:

- Data preprocessing
- Feature engineering
- Model training
- Model evaluation
- MLflow experiment tracking
- Model registry integration
- FastAPI model serving
- Business fraud prediction endpoint
- Dockerized inference service

The ML service loads model artifacts and exposes prediction APIs for the backend gateway.

## MLOps Capabilities

This project demonstrates several MLOps and platform engineering practices:

- Reproducible model training
- Model artifact management
- MLflow tracking and registry
- API-based model serving
- Containerized services
- Full-stack Docker Compose orchestration
- CI/CD-ready monorepo structure
- Monitoring-ready service layout
- Kubernetes-ready infrastructure directory

## Monitoring

The infrastructure includes monitoring configuration for:

- Prometheus
- Grafana
- ML service metrics

Monitoring configuration is located in:

```text
infrastructure/monitoring/
```

## Current Project Status

Completed phases:

```text
17 Monorepo Restructure                  ✅
18 NestJS Backend + PostgreSQL + Prisma  ✅
19 Register/Login + Dashboard UI         ✅
20 Backend Prediction Gateway            ✅
21 Transaction History UI                ✅
22 Backend + Frontend Cleanup            ✅
23 Full-stack Docker Compose Update      ✅
```

Upcoming phases:

```text
24 Full-stack GitHub Actions CI Update
25 Kubernetes Full-stack Update
26 Observability v2
27 ML Monitoring v2
28 Automated Retraining
29 Azure / Cloud Deployment
30 Production README + Architecture
```

## Security Notes

This project currently uses development credentials for local Docker Compose testing. For production deployment:

- Replace all default database credentials
- Use strong JWT secrets
- Store secrets in a secure secret manager
- Enable HTTPS
- Restrict CORS origins
- Add rate limiting
- Add request logging and audit logs
- Use production-grade database backups
- Avoid committing real `.env` files

## Author

Punith Achintha

BSc (Hons) Software Engineering Graduate  
Full-Stack Developer | MLOps and AI Infrastructure Enthusiast