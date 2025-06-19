FROM python:3.9-slim

# Install system dependencies for audio processing and ML
RUN apt-get update && apt-get install -y \
    ffmpeg \
    azure-cli \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download Whisper model during build (optional - reduces startup time)
RUN python -c "import whisper; whisper.load_model('tiny.en')"

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose ports for Streamlit and FastAPI
EXPOSE 8501 8000

# Create startup script
COPY --chown=appuser:appuser deployment/azure/start.sh ./start.sh
RUN chmod +x start.sh

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Start both services
CMD ["./start.sh"]
