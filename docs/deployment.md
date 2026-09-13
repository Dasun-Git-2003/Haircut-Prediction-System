# Deployment Guide

## Docker Setup
The application is fully dockerized.

```bash
docker build -t styleai-backend ./backend
docker run -p 8000:8000 --env-file ./backend/.env styleai-backend
```

## Environment Variables
- `DATABASE_URL`: Connection string
- `JWT_SECRET`: Secret key
- `GENAI_PROVIDER`: "openai" or "stablediffusion"
- `OPENAI_API_KEY`: API key for generative tasks
