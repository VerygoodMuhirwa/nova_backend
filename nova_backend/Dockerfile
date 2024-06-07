# Stage 1: Build dependencies
FROM python:3.11.1 AS builder

ENV PYTHONBUFFERED 1
WORKDIR /code

COPY requirements.txt /code/
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

# Stage 2: Final image
FROM python:3.11.1

ENV PYTHONBUFFERED 1
WORKDIR /code

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /code /code

EXPOSE 8000

# Install Redis server and Daphne
RUN apt-get update && apt-get install -y redis-server && \
    pip install daphne

# Start Redis server and run the backend application with Daphne
CMD service redis-server start && daphne -p 8000 nova_backend.asgi:application & python manage.py runserver 0.0.0.0:8000
