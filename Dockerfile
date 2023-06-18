FROM python:3.11
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY r.txt /app/r.txt
RUN pip install -r r.txt
COPY . /app