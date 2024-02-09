FROM alpine:latest

WORKDIR /vps

ENV VPS_DB_HOST "10.0.0.20"


RUN apk add python3-dev py3-pip

RUN apk add gcc coreutils build-base uwsgi-python3 linux-headers pcre-dev openssl-dev py3-openssl uwsgi-sslrouter


RUN pip3 install --upgrade pip wheel setuptools pyyaml --break-system-packages
RUN pip3 install flask wheel mysql-connector-python flask-bootstrap flask-login  --break-system-packages
RUN pip3 install uwsgi --break-system-packages
#
#CMD ["python3", "/vps/router.py"]

CMD ["uwsgi", "--ini", "uwsgi.ini", "--chdir", "/vps", "--plugin", "python3"]
