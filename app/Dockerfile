# syntax=docker/dockerfile:1
FROM python:3.7-alpine
LABEL mantainer="valande@gmail.com"

RUN apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers

WORKDIR /code
COPY requirements.txt requirements.txt
RUN ls -l && pip install -r requirements.txt

ENV FLASK_APP=valapp.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
