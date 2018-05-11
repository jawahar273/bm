

web: daphne config.asgi:application -p $PORT -b $HOST -v2
worker: celery -A bm.taskapp.celery worker -E  --loglevel=info
