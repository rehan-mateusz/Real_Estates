FROM python:3.5-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add zlib-dev jpeg-dev gcc musl-dev
RUN pip install -r /requirements.txt

RUN mkdir /estate_project
WORKDIR /estate_project
COPY /estate_pro /estate_project/

RUN adduser -D user
USER user

EXPOSE 8000
