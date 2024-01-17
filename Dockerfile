FROM alpine:latest

WORKDIR /vps

ADD router.py .
ADD lib/ .
ADD ssl/ .

RUN apk add nginx
RUN apk add python3 py3-pip

RUN pip3 install flask uwsgi wheel

CMD ["python3", "/vps/router.py"]