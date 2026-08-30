FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code (NOT data — data is mounted as volume)
COPY model/ ./model/
COPY train/ ./train/
COPY data/ ./data/
COPY eval/ ./eval/
COPY server/ ./server/
COPY client/ ./client/
COPY demo/ ./demo/
COPY utils/ ./utils/

# Create logs directory
RUN mkdir -p logs

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

CMD ["python", "demo/week1_demo.py"]
