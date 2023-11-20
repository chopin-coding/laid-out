#!/bin/sh

sudo systemctl start postgresql
sudo systemctl start redis
npm run build
python ./manage.py collectstatic --noinput
python ./manage.py runserver 0.0.0.0:8000 --settings laid_out.settings-dev-build &
DJANGO_SETTINGS_MODULE=laid_out.settings-dev-build celery -A laid_out worker -l INFO