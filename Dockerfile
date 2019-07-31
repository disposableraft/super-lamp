FROM python:3.7-slim-stretch

COPY ./app /app

RUN apt-get update \
    && apt-get install -y python3-dev gcc nodejs curl \
    && pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/* 

RUN pip install -r /app/server/requirements.txt

# Install Node, Yarn and build the client
WORKDIR /app/client

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
    && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list

RUN apt-get update \
    && apt-get install yarn \
    && yarn install \
    && yarn build

EXPOSE 80

WORKDIR /app/server

CMD ["python", "/app/server/app.py"]
