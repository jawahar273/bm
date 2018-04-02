
web: gunicorn config.wsgi --log-file -
worker: celery -A bm.taskapp worker -S django -l info
web: celery flower -A bm.taskapp --port=$PORT --broker=$BROKER_URL --db=$DATABASE_URL --persistent=true