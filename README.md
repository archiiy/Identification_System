# AI-Based KYC Verification System

AI-powered identity verification platform built using OCR, face matching, liveness detection, and centralized logging.

## Features

* Aadhaar OCR extraction
* Profile extraction
* Aadhaar checksum validation
* Face matching using embeddings
* Liveness detection
* Centralized logging with Elasticsearch & Kibana
* Docker-based monitoring

## Tech Stack

Frontend:

* Angular
* TypeScript
* HTML
* CSS

Backend:

* FastAPI
* Python

AI / Computer Vision:

* PaddleOCR
* InsightFace
* MediaPipe
* OpenCV

Monitoring:

* Elasticsearch
* Kibana

Containerization:

* Docker

---

## Project Setup

### 1. Clone Repository

```bash
git clone <your-repo-url>

cd IDENTIFICATION-SYSTEM
```

---

### 2. Backend Setup

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.app:app --reload
```

Backend:

```plaintext
http://localhost:8000
```

Swagger:

```plaintext
http://localhost:8000/docs
```

---

### 3. Frontend Setup

```bash
cd frontend

npm install

ng serve
```

Frontend:

```plaintext
http://localhost:4200
```

---

### 4. Elastic Stack Setup

Start Docker:

```bash
docker start elastic

docker start kibana
```

OR

```bash
docker compose up -d
```

Elasticsearch:

```plaintext
http://localhost:9200
```

Kibana:

```plaintext
http://localhost:5601
```

---

## API Endpoints

```http
POST /verify-aadhaar
POST /verify-selfie
POST /verify-live
```

---

## Monitoring

Logs are stored in:

```plaintext
verification-logs
```

Open:

```plaintext
http://localhost:5601/app/discover
```

---

## Author

Archita
