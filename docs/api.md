# API Documentation

## Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Get JWT token

## Users
- `GET /api/users/profile` - Get current user profile

## Analysis
- `POST /api/analysis/upload` - Upload an image
- `POST /api/analysis/analyze/{session_id}` - Trigger ML analysis

## Recommendations
- `POST /api/recommendations/` - Get haircut recommendations

## TryOn
- `POST /api/tryon/generate` - Generate virtual try-on image

## Hairstyles
- `GET /api/hairstyles/` - List available hairstyles
