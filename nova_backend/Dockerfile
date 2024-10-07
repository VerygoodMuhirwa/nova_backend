# Stage 1: Builder
FROM python:3.11.1 AS builder
ENV PYTHONBUFFERED 1
WORKDIR /code

# Create virtual environment and upgrade pip & setuptools
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip setuptools

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libatlas-base-dev \
    gfortran \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
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
    alsa-utils \
    redis-server \
    daphne \
    libgl1-mesa-glx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up ALSA to use a dummy audio device
RUN echo "pcm.!default { type plug slave.pcm { type hw card 0 } }" > /etc/asound.conf && \
    echo "ctl.!default { type hw card 0 }" >> /etc/asound.conf

# Start PulseAudio in the background and create a virtual sink
RUN pulseaudio --start && pactl load-module module-null-sink sink_name=Virtual_Sink

# Copy site-packages from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy the project code including manage.py
COPY . /code

# Expose port 8000 for the application
EXPOSE 8000

# Start Redis server, PulseAudio, Daphne, and Django server
CMD service redis-server start && \
    pulseaudio --start && \
    daphne -p 8000 nova_backend.asgi:application & \
    python manage.py runserver 0.0.0.0:8000
