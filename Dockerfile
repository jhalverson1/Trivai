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

# Create initialization scripts
RUN echo 'from database import engine; from models import Base; Base.metadata.create_all(bind=engine)' > init_db.py && \
    echo 'from database import SessionLocal; from models import Difficulty; \
    db = SessionLocal(); \
    if not db.query(Difficulty).count(): \
        difficulties = [ \
            Difficulty(id=1, name="Beginner", description="Basic knowledge questions suitable for beginners"), \
            Difficulty(id=2, name="Easy", description="Simple questions with straightforward answers"), \
            Difficulty(id=3, name="Medium", description="Moderate difficulty requiring good general knowledge"), \
            Difficulty(id=4, name="Hard", description="Challenging questions for knowledgeable players"), \
            Difficulty(id=5, name="Expert", description="Very difficult questions for trivia experts") \
        ]; \
        db.add_all(difficulties); \
        db.commit(); \
        db.close()' > seed_db.py

# Update CORS settings for Railway domain
ENV CORS_ORIGIN="https://*.railway.app"
ENV PORT=8080
EXPOSE $PORT

# Run migrations and start server
CMD bash -c '\
    echo "Waiting for database..." && \
    sleep 5 && \
    echo "Running database initialization..." && \
    python init_db.py && \
    echo "Running Alembic migrations..." && \
    alembic upgrade head && \
    echo "Seeding initial data..." && \
    python seed_db.py && \
    echo "Starting server..." && \
    python server.py'