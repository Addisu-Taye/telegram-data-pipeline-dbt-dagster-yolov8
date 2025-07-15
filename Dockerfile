# File Path: Dockerfile
# Date: 10 July 2025
# Developed by: Addisu Taye Dadi
# Purpose: Define the containerized Python application image.
# Key Features:
# - Sets up Python environment inside Docker.
# - Copies source code and installs dependencies.

FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["echo", "Container built successfully"]