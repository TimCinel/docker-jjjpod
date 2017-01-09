FROM python:2.7-alpine
MAINTAINER Tim Cinel <email@timcinel.com>

RUN apk add --no-cache --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ gosu

RUN apk --update add build-base linux-headers \
    && pip install uwsgi \
    && apk del -r build-base linux-headers \
    && rm -rf /var/cache/apk/*

RUN mkdir -p /opt/jjjPod
WORKDIR /opt/jjjPod

COPY src/*.py /opt/jjjPod/
COPY uwsgi.ini /opt/jjjPod/

EXPOSE 3031
CMD uwsgi uwsgi.ini
