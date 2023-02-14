# ----------------------------------------------------------------------
FROM python:3.9.16-alpine3.17 as compile-stage

RUN apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers

WORKDIR /code
COPY requirements.txt ./requirements.txt
RUN pip install --prefix=/pyinstall -r requirements.txt 
    
# ----------------------------------------------------------------------
FROM python:3.7-alpine as runtime

LABEL version=1.0-beta \
      description="Imagen para practica Contenedores y Kubernetes" \
      mantainer="Valande <valande@gmail.com>"

COPY --from=compile-stage /pyinstall /usr/local
WORKDIR /code
COPY . ./
RUN rm ./requirements.txt && \
    addgroup -S appuser && \
    adduser -S appuser -G appuser && \
    chown -R appuser:appuser /code

USER appuser

ENV FLASK_APP=valapp.py
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
EXPOSE 5000

CMD ["flask", "run"]
