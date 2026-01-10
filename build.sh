#!/usr/bin/env bash

# Upgrade pip
pip install --upgrade pip

# Install all dependencies from requirements.txt
pip install -r requirements.txt

# Collect static files for production
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate