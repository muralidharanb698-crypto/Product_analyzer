#!/usr/bin/env bash

pip install -r requirements.txt

playwright install chromium

cd backend

python manage.py migrate

python manage.py collectstatic --noinput