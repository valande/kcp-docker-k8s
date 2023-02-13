# syntax=docker/dockerfile:1
FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=valapp.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY ./app/requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY ./app .
CMD ["flask", "run"]
