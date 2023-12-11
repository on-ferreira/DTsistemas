# Stage 1: Build Dependencies
FROM python:3.11.7-alpine3.18 AS builder

COPY ./requirements.txt /requirements.txt

RUN python -m venv /py \
    && /py/bin/pip install --upgrade pip \
    && apk add --update --no-cache postgresql-dev \
    && /py/bin/pip install -r /requirements.txt

# Stage 2: Create Final Image
FROM python:3.11.7-alpine3.18

LABEL maintainer="DTsistemas"

ENV PYTHONBUFFERED 1

COPY --from=builder /py /py
COPY ./main_project /main_project

WORKDIR /main_project
EXPOSE 5095

ENV PATH="/py/bin:$PATH"

RUN adduser --disabled-password --no-create-home DTuser && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R DTuser:DTuser /vol  && \
    chmod -R 755 /vol

USER DTuser
