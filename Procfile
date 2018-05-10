
web: daphne config.asgi:application --port $PORT
worker: celery -A bm.taskapp.celery worker -E  --loglevel=info
