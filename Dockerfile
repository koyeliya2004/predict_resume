FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend files
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_sm

# Copy rest of backend
COPY backend/ .

# Pre-download BERT model so cold start is faster
RUN python -c "from transformers import pipeline; pipeline('ner', model='dslim/bert-base-NER', grouped_entities=True)" || true

# Expose port 7860 (HF Spaces default)
EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
