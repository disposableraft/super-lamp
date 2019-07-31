FROM python:3.7-slim-stretch

RUN apt-get update \
    && apt-get install -y python3-dev gcc \
    && pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/* 

COPY ./app /app

RUN pip install -r /app/server/requirements.txt

EXPOSE 80

WORKDIR /app/server

CMD ["python", "/app/server/app.py"]
