FROM node:16 AS frontend
WORKDIR /front
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
CMD npm run start

FROM python:3.9-slim AS backend
WORKDIR /app
RUN apt-get update && apt-get install -y \
    libgl1-mesa-dev \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
COPY ./app /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
