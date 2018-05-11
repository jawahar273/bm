

web: daphne config.asgi:application -p $PORT -b 0.0.0.0 -v2
worker: celery -A bm.taskapp.celery worker -E  --loglevel=info
