FROM python:3.10-slim-bullseye

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app

EXPOSE 5000
CMD ["python3", "server.py"]