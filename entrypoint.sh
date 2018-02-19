#!/bin/sh
#python manage.py makemigrations ppsus_app
python manage.py migrate
#python initadmin.py
uwsgi --http :8000 --module ppsus.wsgi
