FROM python:3.12-slim


# PYTHON CONFIGURATION

# Prevent Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Enable real-time Python logs
ENV PYTHONUNBUFFERED=1

# Make project modules importable
ENV PYTHONPATH=/app


# WORKING DIRECTORY

WORKDIR /app


# SYSTEM DEPENDENCIES

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc && \
    rm -rf /var/lib/apt/lists/*


# PYTHON DEPENDENCIES

# Copy requirements first
# This improves Docker layer caching

COPY requirements.txt .


# Upgrade pip and install dependencies

RUN pip install \
    --no-cache-dir \
    --upgrade pip && \
    pip install \
    --no-cache-dir \
    -r requirements.txt


# APPLICATION SOURCE CODE

# Copy API
COPY api ./api

# Copy source code
COPY src ./src

# Copy models directory
# Local model fallback will be available here

COPY models ./models


# APPLICATION DATA

# Create data directory
# Dataset is mounted by docker-compose

RUN mkdir -p /app/data


# PORT

EXPOSE 8000


# DEFAULT APPLICATION

# Default command starts FastAPI.
#
# Trainer overrides this command through
# docker-compose.yml.

# Start FastAPI application

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]