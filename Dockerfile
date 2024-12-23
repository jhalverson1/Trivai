# Frontend build stage
FROM node:18-alpine AS frontend-builder
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
ARG REACT_APP_API_URL
ENV REACT_APP_API_URL=$REACT_APP_API_URL
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
ENV PORT=8080
EXPOSE $PORT

# Create a startup script
RUN echo '#!/bin/bash\n\
echo "Waiting for database..."\n\
sleep 5\n\
echo "Running migrations..."\n\
alembic upgrade head || exit 1\n\
echo "Starting server..."\n\
exec python server.py' > /app/start.sh

RUN chmod +x /app/start.sh
CMD ["/app/start.sh"]