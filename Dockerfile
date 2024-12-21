# Frontend build stage
FROM node:18-alpine AS frontend-builder
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
ENV REACT_APP_API_URL=https://trivai-production-1311.up.railway.app
RUN npm run build

# Backend stage
FROM python:3.11-slim
WORKDIR /app

# Copy backend files
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .

# Copy frontend build
COPY --from=frontend-builder /frontend/build /app/static

# Update CORS settings for Railway domain
ENV CORS_ORIGIN="https://*.railway.app"

# Remove default DATABASE_URL to ensure Railway's is used
ENV PORT=8080
EXPOSE $PORT

# Create required directories and initialize alembic
RUN mkdir -p alembic/versions

# Run migrations and start server with proper error handling
CMD bash -c '\
    echo "Waiting for database..." && \
    sleep 5 && \
    echo "Running database initialization..." && \
    python -c "\
    from database import engine; \
    from models import Base; \
    Base.metadata.create_all(bind=engine)" && \
    echo "Running Alembic migrations..." && \
    alembic upgrade head && \
    echo "Seeding initial data..." && \
    python -c "\
    from database import SessionLocal; \
    from models import Difficulty; \
    db = SessionLocal(); \
    if not db.query(Difficulty).count(): \
        difficulties = [ \
            Difficulty(id=1, name=\"Beginner\", description=\"Basic knowledge questions suitable for beginners\"), \
            Difficulty(id=2, name=\"Easy\", description=\"Simple questions with straightforward answers\"), \
            Difficulty(id=3, name=\"Medium\", description=\"Moderate difficulty requiring good general knowledge\"), \
            Difficulty(id=4, name=\"Hard\", description=\"Challenging questions for knowledgeable players\"), \
            Difficulty(id=5, name=\"Expert\", description=\"Very difficult questions for trivia experts\") \
        ]; \
        db.add_all(difficulties); \
        db.commit(); \
        db.close()" && \
    echo "Starting server..." && \
    python server.py'