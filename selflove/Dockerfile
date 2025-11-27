# Use an official Python runtime as a parent image
FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER=/usr/bin/chromedriver \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=9999

RUN apt-get update && apt-get install -y --no-install-recommends \
      ca-certificates \
      wget \
      gnupg \
      unzip \
      fonts-liberation \
      libnss3 \
      libatk1.0-0 \
      libatk-bridge2.0-0 \
      libcups2 \
      libx11-xcb1 \
      libxcomposite1 \
      libxcursor1 \
      libxdamage1 \
      libxrandr2 \
      libxss1 \
      libasound2 \
      libgbm1 \
      libgtk-3-0 \
      procps \
      build-essential \
      curl \
    && rm -rf /var/lib/apt/lists/*

# https://datawookie.dev/blog/2023/12/chrome-chromedriver-in-docker/
RUN apt-get update -qq -y && \
    apt-get install -y \
        libasound2 \
        libatk-bridge2.0-0 \
        libgtk-4-1 \
        libnss3 \
        xdg-utils \
        wget && \
    wget -q -O chrome-linux64.zip https://bit.ly/chrome-linux64-121-0-6167-85 && \
    unzip chrome-linux64.zip && \
    rm chrome-linux64.zip && \
    mv chrome-linux64 /opt/chrome/ && \
    ln -s /opt/chrome/chrome /usr/local/bin/ && \
    wget -q -O chromedriver-linux64.zip https://bit.ly/chromedriver-linux64-121-0-6167-85 && \
    unzip -j chromedriver-linux64.zip chromedriver-linux64/chromedriver && \
    rm chromedriver-linux64.zip && \
    mv chromedriver /usr/local/bin/

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 40111

CMD ["python", "app.py"]