FROM alpine:latest

WORKDIR /vps

ENV VPS_DB_HOST "10.0.0.20"

#COPY router.py .
#COPY lib/ lib/
#COPY ssl/ ssl/
#COPY templates/ templates/

RUN apk add nginx
RUN apk add python3 py3-pip

RUN apk add gcc coreutils build-base uwsgi-python3


RUN pip3 install --upgrade pip wheel setuptools  --break-system-packages
RUN pip3 install flask wheel mysql-connector-python flask-bootstrap flask-login  --break-system-packages

CMD ["python3", "/vps/router.py"]
