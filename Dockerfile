FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directories
RUN mkdir -p data vector_store

# Expose ports
EXPOSE 8501 8000

# Run Streamlit
CMD ["streamlit", "run", "app/main_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]