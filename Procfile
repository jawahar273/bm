

web: daphne config.asgi:application -p $PORT -v2
worker: celery -A bm.taskapp.celery worker -E  --loglevel=info
