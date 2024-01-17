FROM alpine:latest

WORKDIR /vps

ADD router.py .
ADD lib/ .
ADD ssl/ .

RUN apk add nginx
RUN apk add python3 py3-pip

RUN apk add gcc coreutils build-base uwsgi-python3

RUN python3 -m venv venv

RUN venv/bin/pip3 install --upgrade pip wheel setuptools
RUN venv/bin/pip3 install flask wheel

CMD ["venv/bin/python3", "/vps/router.py"]