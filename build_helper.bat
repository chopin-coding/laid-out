call npm run build
call py ./manage.py collectstatic --noinput
call py ./manage.py runserver