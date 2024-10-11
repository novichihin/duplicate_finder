FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-tk \
    libx11-6 \
    libxft2 \
    libxext6 \
    libxrender1 \
    && apt-get clean

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
