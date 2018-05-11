

web: daphne config.asgi:application
worker: celery -A bm.taskapp.celery worker -E  --loglevel=info
