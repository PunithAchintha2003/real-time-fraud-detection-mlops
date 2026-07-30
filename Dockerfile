FROM python:3.12-slim


# PYTHON CONFIGURATION

# Prevent Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Enable real-time Python logs
ENV PYTHONUNBUFFERED=1

# Make project modules importable
ENV PYTHONPATH=/app

# Reduce MLflow Git warning noise
ENV GIT_PYTHON_REFRESH=quiet


# WORKING DIRECTORY

WORKDIR /app


# SYSTEM DEPENDENCIES

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    git && \
    rm -rf /var/lib/apt/lists/*


# PYTHON DEPENDENCIES

COPY requirements.txt .

COPY pytest.ini .


RUN pip install \
    --no-cache-dir \
    --upgrade pip && \
    pip install \
    --no-cache-dir \
    -r requirements.txt


# APPLICATION SOURCE CODE

# Copy FastAPI application
COPY api ./api

# Copy ML source code
COPY src ./src

# Copy trained local models
COPY models ./models

# Copy automated tests
COPY tests ./tests


# APPLICATION DATA

RUN mkdir -p /app/data


# PORT

EXPOSE 8000


# DEFAULT APPLICATION

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]