
web: gunicorn config.wsgi --log-file -
celeryd: celery -A task worker -E  --loglevel=info info
