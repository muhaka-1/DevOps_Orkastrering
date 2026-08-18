# JensenStore API

Small Flask API used for a CI/CD exercise.

## Endpoints
- `GET /`        -> {"application":"JensenStore API","status":"running","version":"1.0.0"}
- `GET /health`  -> {"status":"healthy"}

## Run locally
    python -m pip install -r requirements.txt
    python -m pytest -q
    python app.py
