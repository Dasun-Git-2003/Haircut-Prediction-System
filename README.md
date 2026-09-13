# StyleAI: AI-Powered Hairstyle Recommendation & Virtual Try-On

StyleAI is an advanced web application that utilizes machine learning and generative AI to analyze a user's face shape and hair profile, recommend suitable hairstyles, and virtually apply them to the user's photo.

## Features
- **Face Analysis**: Detects facial landmarks and classifies face shape.
- **Hair Analysis**: Identifies hair type, length, density, and volume.
- **Recommendation Engine**: Scores hairstyles based on facial geometry and user preferences.
- **Virtual Try-On**: GenAI integration (OpenAI/Stable Diffusion) to overlay haircuts.

## Architecture
See [Architecture Docs](docs/architecture.md)

## Tech Stack
- **Backend**: FastAPI, SQLAlchemy, PyTorch, OpenCV, SQLite/PostgreSQL
- **Frontend**: React (Planned)

## Installation

### Local Setup
1. Clone the repository.
2. `cd backend`
3. Create virtual environment: `python -m venv venv`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in API keys.
6. Run the server: `uvicorn app.main:app --reload`

### Docker Deployment
```bash
docker build -t styleai-backend ./backend
docker run -p 8000:8000 --env-file ./backend/.env styleai-backend
```

## ML Training
The models are designed to be trained on the **Figaro1k** dataset. Check `docs/ml.md` for details.

## Documentation
- [API Endpoints](docs/api.md)
- [Deployment](docs/deployment.md)
- [ML Pipeline](docs/ml.md)

## Testing
Run pytest from the backend directory:
```bash
pytest
```

## License
MIT
