# Stage 1: Builder
FROM python:3.11.1 AS builder
ENV PYTHONBUFFERED=1
WORKDIR /code

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libatlas-base-dev \
    gfortran \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/
RUN python -m pip install --upgrade pip setuptools
RUN pip install --no-cache-dir --timeout=120 -r requirements.txt


# Stage 2: Final image
FROM python:3.11.1
ENV PYTHONBUFFERED=1
WORKDIR /code

# Copy site-packages from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy the project code including manage.py
COPY . /code

# Install Redis server and Daphne
RUN apt-get update && apt-get install -y redis-server daphne libgl1-mesa-glx && apt-get clean

EXPOSE 8000

CMD ["sh", "-c", "service redis-server start && daphne -p 8000 nova_backend.asgi:application"]
