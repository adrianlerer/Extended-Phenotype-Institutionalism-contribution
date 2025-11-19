# Legal Evolution Unified - Docker Container
# Multi-stage build adapted from peralta-metamorphosis

# Stage 1: Base Python environment with system dependencies
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Essential build tools
    build-essential \
    gcc \
    g++ \
    # Graphics and plotting dependencies
    libfreetype6-dev \
    libpng-dev \
    libjpeg-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    # Network tools
    curl \
    wget \
    # Git for version control
    git \
    # Additional utilities
    unzip \
    vim \
    nano \
    htop \
    # Clean up
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Development environment with Jupyter and full dependencies
FROM base as development

# Set working directory
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Install additional Jupyter extensions and tools
RUN pip install --no-cache-dir \
    jupyterlab-git \
    jupyter-dash \
    voila

# Create necessary directories
RUN mkdir -p /app/data /app/notebooks /app/code /app/src /app/results /app/docs /app/visualizations

# Copy project files
COPY . .

# Set up Jupyter configuration
RUN jupyter lab --generate-config && \
    echo "c.ServerApp.ip = '0.0.0.0'" >> ~/.jupyter/jupyter_lab_config.py && \
    echo "c.ServerApp.port = 8888" >> ~/.jupyter/jupyter_lab_config.py && \
    echo "c.ServerApp.open_browser = False" >> ~/.jupyter/jupyter_lab_config.py && \
    echo "c.ServerApp.allow_root = True" >> ~/.jupyter/jupyter_lab_config.py && \
    echo "c.ServerApp.token = ''" >> ~/.jupyter/jupyter_lab_config.py && \
    echo "c.ServerApp.password = ''" >> ~/.jupyter/jupyter_lab_config.py

# Create startup script
RUN echo '#!/bin/bash\n\
echo "Starting Legal Evolution Unified Environment..."\n\
echo "Jupyter Lab: http://localhost:8888"\n\
echo "API: http://localhost:8000"\n\
echo "Dashboard: http://localhost:8050"\n\
echo "Neo4j Browser: http://localhost:7474"\n\
echo ""\n\
echo "Available services:"\n\
echo "  - JurisRank: Legal fitness calculation"\n\
echo "  - RootFinder: Genealogy tracking"\n\
echo "  - Iusmorfos: Transplant prediction"\n\
echo "  - Peralta: Network analysis & bootstrap validation"\n\
echo ""\n\
exec "$@"' > /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

# Expose ports
EXPOSE 8888 8050 8000

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command
CMD ["jupyter", "lab", "--allow-root", "--no-browser", "--ip=0.0.0.0", "--port=8888"]

# Stage 3: Production environment (minimal)
FROM base as production

# Install only essential production dependencies
WORKDIR /app
COPY requirements.txt .

# Install minimal production requirements
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    numpy pandas scipy scikit-learn \
    networkx matplotlib plotly \
    fastapi uvicorn gunicorn \
    neo4j redis python-dotenv

# Copy only necessary files
COPY code/ ./code/
COPY src/ ./src/
COPY data/ ./data/
COPY setup.py .
COPY README.md .

# Install the package
RUN pip install -e .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash legaluser && \
    chown -R legaluser:legaluser /app

USER legaluser

# Expose port for API
EXPOSE 8000

# Production command (FastAPI via gunicorn)
CMD ["gunicorn", "src.api.main:app", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker"]

# Labels for metadata
LABEL maintainer="Legal Evolution Unified Project" \
      description="Integrated Legal Concept Evolution Analysis Platform" \
      version="1.0.0" \
      license="MIT" \
      repository="https://github.com/adrianlerer/legal-evolution-unified"
