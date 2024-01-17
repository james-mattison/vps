FROM alpine:latest

WORKDIR /vps

COPY router.py .
COPY lib/ lib/
COPY ssl/ ssl/
COPY templates/ templates/

RUN apk add nginx
RUN apk add python3 py3-pip

RUN apk add gcc coreutils build-base uwsgi-python3

RUN python3 -m venv venv

RUN venv/bin/pip3 install --upgrade pip wheel setuptools
RUN venv/bin/pip3 install flask wheel mysql-connector-python flask-bootstrap flask-login

CMD ["venv/bin/python3", "/vps/router.py"]