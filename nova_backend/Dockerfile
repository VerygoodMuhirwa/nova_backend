# Stage 1: Builder
FROM python:3.11.1 AS builder
ENV PYTHONBUFFERED 1
WORKDIR /code

RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip setuptools

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libatlas-base-dev \
    gfortran \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt --verbose

# Stage 2: Final image
FROM python:3.11.1
ENV PYTHONBUFFERED 1
WORKDIR /code

# Install required packages including PulseAudio
RUN apt-get update && apt-get install -y --no-install-recommends \
    pulseaudio \
    pulseaudio-utils \
    redis-server \
    daphne \
    libgl1-mesa-glx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Start PulseAudio in the background and create a virtual sink
RUN pulseaudio --start && pactl load-module module-null-sink sink_name=Virtual_Sink

# Copy site-packages from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
# Copy the project code including manage.py
COPY . /code
EXPOSE 8000


CMD service redis-server start && \
    pulseaudio --start && \
    daphne -p 8000 nova_backend.asgi:application & \
    python manage.py runserver 0.0.0.0:8000
