

web: daphne config.asgi:application --port $PORT --bind $HOST
worker: celery -A bm.taskapp.celery worker -E  --loglevel=info
