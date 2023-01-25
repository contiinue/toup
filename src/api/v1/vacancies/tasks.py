from config.celery import app
from .get_vacancies import get_vacancies
import asyncio


@app.task
def task_to_get_vacancies():
    asyncio.run(get_vacancies())
