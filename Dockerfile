FROM python:2.7-alpine
MAINTAINER Tim Cinel <email@timcinel.com>

RUN apk --update add build-base linux-headers \
    && pip install uwsgi \
    && apk del -r build-base linux-headers \
    && rm -rf /var/cache/apk/*

RUN mkdir -p /opt/jjjPod
WORKDIR /opt/jjjPod

ADD files/*.py /opt/jjjPod/
ADD files/uwsgi.ini /opt/jjjPod/

RUN mkdir -p /etc/nginx/locations.d/timcinel/
ADD files/nginx-location.conf /etc/nginx/locations.d/timcinel/

EXPOSE 3031
CMD uwsgi uwsgi.ini
