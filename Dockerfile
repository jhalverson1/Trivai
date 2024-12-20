# Frontend build stage
FROM node:18-alpine AS frontend-builder
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
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

ENV PORT=8000
EXPOSE $PORT
CMD ["python", "server.py"] 