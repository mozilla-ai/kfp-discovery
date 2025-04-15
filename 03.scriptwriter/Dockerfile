ARG BASE_IMAGE=dpoulopoulos/doc-to-podcast-base
ARG BASE_TAG=latest
FROM ${BASE_IMAGE}:${BASE_TAG}

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY scriptwriter.py . 
