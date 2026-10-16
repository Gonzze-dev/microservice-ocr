# Build context: repo root (docker build -f infra.prod/Dockerfile .)
# En Railway: RAILWAY_DOCKERFILE_PATH=infra.prod/Dockerfile

FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install poetry

# The app gets its own venv so its dependencies don't get mixed with Poetry's
# (requests, charset-normalizer...) in the system site-packages.
ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"
RUN python -m venv /opt/venv

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi --no-root

COPY src/ ./src/
WORKDIR /app/src

# Downloads the models (license plate detector + PaddleOCR) during the build
# so they are not fetched on every container start.
RUN python -c "from services import LicensePlateDetector, OCR; LicensePlateDetector(); OCR()"

EXPOSE 8000

CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --proxy-headers --forwarded-allow-ips='*'"]
