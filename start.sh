#!/usr/bin/env bash
set -e
python manage.py collectstatic --noinput
python manage.py migrate --noinput
# Launch gunicorn
exec gunicorn django_project.wsgi:application --bind 0.0.0.0:${PORT:-8000}
