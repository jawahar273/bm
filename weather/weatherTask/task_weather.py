from celery.utils.log import get_task_logger

from bm.taskapp.celery import app

@app.task
def get_weather_api():