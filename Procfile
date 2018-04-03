
web: gunicorn config.wsgi --log-file -
worker: celery -A taskapp worker -S django  -l info
