FROM python:3.7-slim-stretch

RUN apt-get update && apt-get install -y python3-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY server/requirements.txt /app/server/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /app/server/requirements.txt

COPY ./server /app/server
COPY ./client /app/client

EXPOSE 80

WORKDIR /app/server

CMD ["python", "/app/server/app.py"]
