#!/bin/sh
#python manage.py makemigrations
python manage.py migrate
uwsgi --http :8000 --module ppsus.wsgi
