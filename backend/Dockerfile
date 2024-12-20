FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Create static directory and add a placeholder index.html
RUN mkdir -p static && \
    echo "<html><body>Development Server</body></html>" > static/index.html

EXPOSE 8000
CMD ["python", "server.py"] 