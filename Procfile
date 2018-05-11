

web: daphne config.asgi:application -v2
worker: celery -A bm.taskapp.celery worker -E  --loglevel=info
