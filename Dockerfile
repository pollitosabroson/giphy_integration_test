FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip

RUN pip install -U -r requirements.txt

COPY ./src /app/src

ENV PYTHONPATH=/app
