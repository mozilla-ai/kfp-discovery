FROM python:3.12.9-slim-bookworm

RUN apt update && \
    apt install -y \
    git \
    cmake \
    build-essential

COPY requirements.txt .

RUN pip install -r requirements.txt
