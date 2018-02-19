#!/bin/sh
#python manage.py makemigrations
python manage.py migrate
#python manage.py createsuperuser
uwsgi --http :8000 --module ppsus.wsgi
