FROM python:3.10-slim-bullseye
ENV PYTHONUNBUFFERED 1
WORKDIR /backend
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .