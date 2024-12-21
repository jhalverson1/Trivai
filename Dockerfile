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

# Create required directories
RUN mkdir -p alembic/versions

# Run migrations and start server with proper error handling
CMD bash -c '\
    echo "Waiting for database..." && \
    sleep 5 && \
    echo "Running migrations..." && \
    alembic upgrade head && \
    echo "Starting server..." && \
    python server.py'