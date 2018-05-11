

web: daphne config.asgi:application --port $PORT --bind $HOST -v2
worker: celery -A bm.taskapp.celery worker -E  --loglevel=info
