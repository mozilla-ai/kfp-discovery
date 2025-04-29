FROM python:3.12.9-slim-bookworm

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        cmake \
        build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip setuptools wheel

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt