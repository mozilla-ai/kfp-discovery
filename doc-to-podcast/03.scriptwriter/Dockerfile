ARG BASE_IMAGE=mzdotai/workflow-components-base-cuda
ARG BASE_TAG=latest
FROM ${BASE_IMAGE}:${BASE_TAG}

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY scriptwriter.py .