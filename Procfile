
web: gunicorn config.wsgi --log-file -
worker: celery -A bm.taskapp worker  -l info
