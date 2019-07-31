FROM python:3.7-slim-stretch

RUN apt-get update \
    && apt-get install -y python3-dev gcc \
    && pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/* 

RUN pip install torch

RUN pip install fastai

COPY ./app/server/requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY ./app /app

EXPOSE 80

WORKDIR /app/server

CMD ["python", "/app/server/app.py"]
