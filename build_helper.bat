call npm run build
call py ./manage.py collectstatic --noinput
call py ./manage.py runserver 0.0.0.0:8000