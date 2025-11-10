# Base Python image
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    DJANGO_SETTINGS_MODULE=mysite.settings_prod

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Project
COPY . .

# Static collection
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Gunicorn
CMD ["gunicorn", "mysite.wsgi:application", "-b", "0.0.0.0:8000", "--workers", "3"]
