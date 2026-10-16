FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

# The app gets its own venv so its dependencies don't get mixed with Poetry's
# (requests, charset-normalizer...) in the system site-packages.
ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"
RUN python -m venv /opt/venv

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY src/ ./src/

EXPOSE 8000

WORKDIR /app/src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
