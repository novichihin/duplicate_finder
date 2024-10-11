FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-tk \
    libx11-6 \
    libxft2 \
    libxext6 \
    libxrender1 \
    xvfb \
    && apt-get clean

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Запуск Xvfb и приложения
CMD rm -f /tmp/.X99-lock && \
    Xvfb :1 -screen 0 1024x768x16 & \
    export DISPLAY=:1 && \
    python3 main.py