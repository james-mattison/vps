FROM alpine:latest

WORKDIR /vps

ENV VPS_DB_HOST "10.0.0.20"


RUN apk add python3-dev py3-pip

RUN apk add gcc coreutils build-base linux-headers pcre-dev openssl-dev py3-openssl py3-gunicorn openssl openssl-dev openssl-libs-static


RUN pip3 install --upgrade pip wheel setuptools pyyaml --break-system-packages
RUN pip3 install flask wheel mysql-connector-python flask-bootstrap flask-login  --break-system-packages
RUN pip3 install gunicorn --break-system-packages
#
#CMD ["python3", "/vps/router.py"]

CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0:80", "--keyfile", "/vps/passthru/ssl/key.pem", "--certfile", "/vps/passthru/ssl/cert.pem", "router:app"]




