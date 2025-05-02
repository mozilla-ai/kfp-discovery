FROM python:3.12.9-slim-bookworm

RUN apt update && \
    apt install -y --no-install-recommends \
        git \
        cmake \
        build-essential && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip setuptools wheel

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt