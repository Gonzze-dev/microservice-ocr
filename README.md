# Microservice OCR — License Plate Reader

REST API microservice developed as part of a thesis project for the automatic detection and recognition of vehicle license plates. Given an image, the service detects the license plate region using a YOLOv9 model and then extracts its alphanumeric text using PaddleOCR.

## How It Works

The processing pipeline consists of two sequential stages:

1. **License Plate Detection** — A YOLOv9 model (`yolo-v9-t-384-license-plate-end2end`) locates and crops the license plate from the input image. A confidence threshold of `0.83` is required for the detection to be considered valid.

2. **Text Extraction (OCR)** — The cropped plate is processed by PaddleOCR (Spanish language model) to extract the alphanumeric text. Words unrelated to the plate itself (e.g. `REPUBLICA ARGENTINA`, `MERCOSUR`) are filtered out automatically.

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI + Uvicorn |
| Detection model | YOLOv9 via `open-image-models` |
| OCR engine | PaddleOCR |
| Image processing | OpenCV, NumPy |
| Containerization | Docker + Docker Compose |
| Dependency management | Poetry |
| Runtime | Python 3.13 |

## API Reference

### `GET /health`

Verifica que el servicio esté en funcionamiento.

**Autenticación:** no requerida.

**Response — `200 OK`:**

```json
{
  "status": "ok"
}
```

---

### `POST /read-license-plate`

Receives an image and returns the detected license plate text.

**Authentication:** requires the `x-api-key` header.

**Request** — `multipart/form-data`:

| Field | Type | Description |
|---|---|---|
| `image` | file | Vehicle image (JPG, PNG, etc.) |

**Success response — `200 OK`:**

```json
{
  "license_plate": "ABC123"
}
```

**Error responses** follow the [RFC 9457 Problem Details](https://www.rfc-editor.org/rfc/rfc9457) standard (`application/problem+json`):

| Status | Title | Cause |
|---|---|---|
| `401` | Unauthorized | Invalid or missing API key |
| `422` | License Plate Detection Failed | No plate found in the image |
| `422` | Low Detection Confidence | Detection confidence below threshold |
| `422` | Text Extraction Failed | OCR could not read the plate text |

## Project Structure

```
src/
├── main.py                  # FastAPI app entry point
├── config.py                # Environment variable loading
├── dependencies.py          # Dependency injection (API key, services)
├── routers/
│   └── license_plate.py     # POST /read-license-plate endpoint
├── services/
│   ├── interfaces.py        # Abstract base classes
│   ├── license_plate_detector.py  # YOLOv9 detection logic
│   └── ocr.py               # PaddleOCR extraction logic
└── errors/
    ├── exceptions.py        # ProblemDetail exception & handler
    ├── auth_errors.py
    ├── lp_detector_errors.py
    ├── license_plate_errors.py
    └── ocr_errors.py
```

## Running with Docker

```bash
# 1. Create the environment file
cp .env.example .env

# 2. Build and start the service
docker compose up --build
```

The API will be available at `http://localhost:8000`.

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `API_KEY` | Secret key used to authenticate requests | `default-api-key-12345` |

Create a `.env` file in the project root:

```env
API_KEY=your-secret-api-key
```

## Running Locally (without Docker)

Requires Python 3.13 and [Poetry](https://python-poetry.org/).

```bash
# Install dependencies
poetry install

# Start the server
cd src
uvicorn main:app --host 0.0.0.0 --port 8000
```
