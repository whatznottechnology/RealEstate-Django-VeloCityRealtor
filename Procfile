release: python manage.py collectstatic --noinput
web: gunicorn Source.wsgi:application --bind 0.0.0.0:$PORT
