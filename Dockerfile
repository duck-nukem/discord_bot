FROM python:alpine

RUN apk add --no-cache \
    gcc \
    musl-dev \
    libjpeg \
    jpeg-dev \
    zlib-dev

COPY . /opt/bot

RUN pip install -r /opt/bot/requirements.txt
