#!/bin/sh
set -e

# Designed to be used with Cloud Run Button, adding sample data

python manage.py migrate
python manage.py loaddata sampledata
python manage.py collectstatic --noinput
