# Deployment Guide: StyleAI

StyleAI can be deployed as containerized services via Docker Compose or run locally for active development.

---

## 1. Quick Start with Docker Compose

Ensure Docker and Docker Compose are installed and running.

```bash
# 1. Clone the repository
git clone https://github.com/Dasun-Git-2003/Haircut-Prediction-System.git
cd Haircut-Prediction-System

# 2. Configure Environment Variables
cp backend/.env.example backend/.env

# 3. Launch PostgreSQL, FastAPI Backend, and React Frontend
docker-compose up --build -d
```

### Services Access:
- **Frontend Application**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000`
- **API Documentation (Swagger)**: `http://localhost:8000/docs`
- **PostgreSQL Database**: `localhost:5432`

---

## 2. Local Development Setup

### 2.1 Backend (FastAPI)
```bash
cd backend

# Create & activate Python virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations & seed data automatically on start
uvicorn app.main:app --reload --port 8000
```

### 2.2 Frontend (React + Vite)
```bash
cd frontend

# Install node dependencies
npm install

# Start Vite dev server with proxy to backend
npm run dev
```
Open `http://localhost:5173` to test the frontend with hot-module reloading.

---

## 3. Environment Variables Reference

| Variable | Default / Example | Purpose |
| :--- | :--- | :--- |
| `DATABASE_URL` | `sqlite+aiosqlite:///./styleai.db` | Async SQLAlchemy database connection string (SQLite for local dev, PostgreSQL for production) |
| `JWT_SECRET` | `your-secret-key-here` | Secret key used to sign and verify JWT authentication tokens |
| `JWT_ALGORITHM` | `HS256` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` (24h) | Token lifespan before refresh required |
| `GENAI_PROVIDER` | `gemini` | Active virtual try-on engine (`gemini`, `openai`, `stable_diffusion`) |
| `GOOGLE_API_KEY` | `AIzaSy...` | API key for Google Gemini image generation and editing |
| `OPENAI_API_KEY` | `sk-...` | API key for OpenAI DALL-E 3 / GPT-4o image generation |
| `STABLE_DIFFUSION_URL` | `http://localhost:7860` | Optional WebUI/API URL for self-hosted Stable Diffusion |
| `UPLOAD_DIR` | `./uploads` | Local directory for storing user photos |
| `GENERATED_DIR` | `./generated` | Local directory for storing generated hairstyle previews |
| `CORS_ORIGINS` | `http://localhost:3000,http://localhost:5173` | Allowed frontend origins for CORS |

---

## 4. Production Hardening Checklist

- [ ] Change `JWT_SECRET` to a high-entropy randomly generated secret.
- [ ] Set `DATABASE_URL` to a secure PostgreSQL instance with SSL enabled.
- [ ] Place backend and frontend behind an Nginx reverse proxy with HTTPS (Let's Encrypt / Cloudflare).
- [ ] Configure automatic expiration or cron cleanup for temporary files in `./uploads` to protect user privacy.
