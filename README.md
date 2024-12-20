# TrivAI - AI-Powered Trivia Game

A trivia game that uses OpenAI's GPT to generate dynamic questions across various categories.

## Prerequisites

- Docker and Docker Compose
- OpenAI API key

## Setup

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd trivai
   ```

2. Set up environment variables:
   ```bash
   # Copy the example env file
   cp backend/.env.example backend/.env

   # Edit the .env file with your values
   # Particularly important:
   # - OPENAI_API_KEY
   ```

3. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8080

## Environment Variables

Required environment variables in `backend/.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| OPENAI_API_KEY | Your OpenAI API key | - |
| DATABASE_URL | PostgreSQL connection string | postgresql://postgres:postgres@db:5432/trivai |
| PORT | Server port | 8080 |
| CORS_ORIGINS | Allowed CORS origins | http://localhost:3000,... |
| REACT_APP_API_URL | Frontend API URL | http://localhost:8080 |

## Development

The project uses:
- Frontend: React
- Backend: FastAPI
- Database: PostgreSQL
- AI: OpenAI GPT-3.5

## Deployment

This project is configured for deployment on Railway. Make sure to:
1. Set up the required environment variables in Railway
2. Connect your GitHub repository
3. Configure the PostgreSQL add-on

## License

[Your chosen license] 