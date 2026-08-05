# Backend API

NestJS backend for authentication, user management, and fraud prediction gateway.

## Responsibilities

- User registration and login
- JWT authentication
- PostgreSQL database access with Prisma
- Protected transaction prediction endpoint
- Gateway between frontend and FastAPI ML service

## Main Endpoints

POST /auth/register
POST /auth/login
GET  /auth/me

POST /transactions/check
GET  /transactions
GET  /transactions/:id

## Local Setup

npm install
cp .env.example .env
npm run prisma:generate
npm run build
npm run start:dev

## Environment Variables

See .env.example.
