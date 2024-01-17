FROM alpine:latest

WORKDIR /vps

RUN apk add nginx
RUN apk add python3 py3-pip

RUN pip3 install flask uwsgi wheel

