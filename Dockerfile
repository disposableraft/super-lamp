FROM python:3.7-slim-stretch

RUN apt-get update \
    && apt-get install -y python3-dev gcc gnupg1 curl apt-transport-https \
    && pip install --upgrade pip \
    && curl -sL https://deb.nodesource.com/setup_10.x | bash - \
    && curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
    && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
    && apt-get update \
    && apt-get install -y yarn nodejs \
    && rm -rf /var/lib/apt/lists/*

# Splitting out fastai and torch because memory issues
RUN pip install torch
RUN pip install fastai

COPY ./app /app

RUN pip install -r /app/server/requirements.txt

# Install Node, Yarn and build the client
WORKDIR /app/client

RUN yarn install -s --non-interactive --no-progress
RUN yarn build

EXPOSE 80

WORKDIR /app/server

CMD ["python", "/app/server/app.py"]
