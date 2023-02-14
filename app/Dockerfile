FROM python:3.7-alpine

LABEL mantainer="valande@gmail.com"

RUN apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers

WORKDIR /code
COPY . .
RUN pip install -r requirements.txt

RUN addgroup -S appuser && \
    adduser -S appuser -G appuser && \
    chown -R appuser:appuser /code

ENV FLASK_APP=valapp.py
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
EXPOSE 5000

USER appuser

CMD ["flask", "run"]
