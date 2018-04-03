
web: gunicorn config.wsgi --log-file -
worker: celery -A task worker -E  --loglevel=info info
