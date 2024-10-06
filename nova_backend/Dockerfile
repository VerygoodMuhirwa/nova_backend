# Stage 1: Builder
FROM python:3.11.1 AS builder
ENV PYTHONBUFFERED 1
WORKDIR /code
COPY requirements.txt /code/
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt --verbose

# Stage 2: Final image
FROM python:3.11.1
ENV PYTHONBUFFERED 1
WORKDIR /code
# Copy site-packages from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
# Copy the project code including manage.py
COPY . /code
EXPOSE 8000
# Install Redis server and Daphne
RUN apt-get update && apt-get install -y redis-server &&  pip install daphne && apt-get -y install daphne
# Start Redis server and run the backend application with Daphne
CMD service redis-server start && daphne -p 8000 nova_backend.asgi:application & python manage.py runserver 0.0.0.0:8000
