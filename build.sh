#!/usr/bin/env bash

set -o errexit

pip install -r requirements.txt

playwright install chromium

cd backend

python manage.py migrate

python manage.py collectstatic --no-input