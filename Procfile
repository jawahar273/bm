
web: gunicorn config.wsgi --log-file -
worker: celery -A bm.taskapp.celery worker -E  --loglevel=info
