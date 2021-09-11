FROM python:3.8-alpine
WORKDIR /app
RUN apk add --no-cache --virtual .build-deps gcc musl-dev
RUN apk add --no-cache uwsgi-python3 libffi-dev jpeg-dev zlib-dev

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

RUN apk del .build-deps

RUN mkdir /var/run/python

CMD [ "uwsgi", "--ini", "uwsgi_docker_dev.ini" ]
