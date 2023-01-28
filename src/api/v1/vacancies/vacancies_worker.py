import json

from django_celery_beat.models import IntervalSchedule, PeriodicTask
from rest_framework.views import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT


def _stop_worker(user_id) -> Response:
    PeriodicTask.objects.get(name=f"Task for: User{user_id}").delete()
    return Response(data={}, status=HTTP_204_NO_CONTENT)


def _start_worker(user_id: int, interval: int) -> Response:
    schedule, created = IntervalSchedule.objects.get_or_create(
        period=IntervalSchedule.HOURS, every=interval
    )
    PeriodicTask.objects.create(
        name=f"Task for: User{user_id}",
        task="api.v1.vacancies.tasks.task_to_get_vacancies",
        interval=schedule,
        kwargs=json.dumps({"user_id": user_id}),
    )
    return Response(data={"interval": interval}, status=HTTP_201_CREATED)


def start_or_stop_worker(user_id: int, data: dict) -> Response:
    if data["do"] == "start":
        return _start_worker(user_id, data["interval"])
    return _stop_worker(user_id)
