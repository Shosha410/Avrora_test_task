FROM python:3.9-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    unzip \
    wget \
    nodejs \
    npm \
    default-jre \
    chromium \
    chromium-driver \
    nano \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g allure-commandline

ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV CHROME_BIN=/usr/bin/chromium

ENV PYTHONPATH=/app

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "run_tests/acceptance_run_tests.py"]