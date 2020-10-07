#!/bin/bash
python manage.py migrate
#python manage.py collectstatic --noinput
exec uwsgi -w suorganizer.wsgi -p 1 --http-socket 0.0.0.0:8000 -T --disable-write-exception --ignore-sigpip --ignore-write-errors