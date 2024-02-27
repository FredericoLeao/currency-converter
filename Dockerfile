FROM python:3.9

RUN apt-get update && apt-get install -y default-mysql-client

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip && pip install -r requirements.txt
