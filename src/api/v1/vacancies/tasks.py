from config.celery import app
from . import get_vacancies
import asyncio


@app.task()
def task_to_get_vacancies(**kwargs):
    loop = asyncio.new_event_loop()
    loop.create_task(get_vacancies.vacancies(kwargs["user_id"]))
    loop.run_forever()


@app.task()
def make_negotiations(user_id: int, id_notification: int):
    asyncio.run(get_vacancies.send_negotiations(user_id, id_notification))
