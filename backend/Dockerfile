FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

ENV PORT=8080
EXPOSE $PORT

RUN echo '#!/bin/bash\n\
set -e\n\
echo "Waiting for database..."\n\
sleep 5\n\
echo "Checking current database state..."\n\
alembic current\n\
echo "Running migrations..."\n\
PYTHONPATH=/app alembic upgrade head\n\
echo "Verifying database schema..."\n\
python verify_db.py\n\
echo "Starting server..."\n\
exec uvicorn server:app --host 0.0.0.0 --port $PORT' > /app/start.sh

RUN chmod +x /app/start.sh
CMD ["/app/start.sh"] 