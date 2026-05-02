#!/bin/bash
set -e

echo "=== EduAI Platform Setup ==="

# 1. Check for Docker and Docker Compose
if ! command -v docker &> /dev/null; then
    echo "Docker could not be found. Please install Docker."
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "Docker Compose could not be found. Please install Docker Compose."
    exit 1
fi

# 2. Check for NVIDIA drivers
if ! command -v nvidia-smi &> /dev/null; then
    echo "WARNING: nvidia-smi could not be found. Triton server may not have GPU access."
fi

# 3. Setup Python environment if needed (for downloading and pre-processing)
if [ ! -d "env" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv env
fi
source env/bin/activate
pip install -r backend/requirements.txt pandas kagglehub torch

# 4. Download ASSISTments dataset (done via preprocess.py, assumed local cache or downloading script)
echo "Running Data Preprocessing..."
python ml/preprocess.py

# 5. Run DKT training if no checkpoint found
if [ ! -f "checkpoints/dkt_best.pt" ]; then
    echo "No checkpoint found. Running DKT training..."
    python ml/train.py
else
    echo "Checkpoint already exists. Skipping training."
fi

# 6. Export model to ONNX
echo "Exporting model to ONNX..."
python ml/export_onnx.py

# 7. Build and launch all containers
echo "Starting containers with Docker Compose..."
docker-compose up --build -d

echo "=== Setup Complete! ==="
echo "EduAI Frontend is running at http://localhost"
echo "EduAI Backend is running at http://localhost:8080"
echo "Triton Server is running at http://localhost:8000"
