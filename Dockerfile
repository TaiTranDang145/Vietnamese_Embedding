FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Copy requirements file first to utilize Docker layer cache
COPY requirements.txt .

# Install dependencies (CPU-only PyTorch and other requirements)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

# Pre-download the SentenceTransformer model during build time
# This speeds up container startup and allows the service to run offline
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('AITeamVN/Vietnamese_Embedding')"

# Copy application code
COPY src/ ./src
COPY config.yaml .
COPY main.py .

# Expose the API port (8080)
EXPOSE 8080

# Run the entrypoint main.py
CMD ["python", "main.py"]
