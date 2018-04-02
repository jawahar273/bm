
web: gunicorn config.wsgi --log-file -
main_worker: celery -A bm.taskapp worker -S django -l info
