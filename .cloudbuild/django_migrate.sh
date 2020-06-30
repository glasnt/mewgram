#!/bin/sh
set -e

python manage.py migrate
python manage.py loaddata sampledata
python manage.py collectstatic --noinput
