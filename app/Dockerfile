FROM python:3.7-alpine

LABEL mantainer="valande@gmail.com"

RUN apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers

WORKDIR /code
COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "run"]
