import aiohttp

from asgiref.sync import sync_to_async

from .utils import _get_user
from config.vacancies_settings import (
    EXPERIENCE_NAMES,
    LINK_TO_VACANCIES,
)
from dataclasses import dataclass
from models.models import Vacancy, Notification
from tbot import main
from user.models import User

__all__ = ("vacancies",)


@dataclass
class ResponseVacancy:
    id: str
    name: str
    company_name: str
    experience: str
    city: str
    alternate_url: str
    schedule: str
    contact_email: str | None = None
    contacts_phones: str | None = None


@dataclass
class InfoNotification:
    id_notification: int
    count_vacancies: int


async def _make_request(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as response:
            return await response.json()


async def _parse_count_page(data: dict) -> int:
    try:
        return data["pages"]
    except KeyError:
        return 0


def _get_id(data: dict) -> str:
    return data["id"]


def _get_name(data: dict) -> str:
    return data["name"]


def _get_company_name(data: dict) -> str:
    return data["employer"]["name"]


def _get_city(data: dict) -> str | None:
    try:
        return data["address"]["city"]
    except TypeError:
        return None


def _get_alternate_url(data: dict) -> str:
    return data["alternate_url"]


def _get_schedule(data: dict) -> str:
    return data["schedule"]["name"]


def get_contact_email(data: dict) -> str | None:
    try:
        return data["contacts"]["email"]
    except TypeError:
        return None


def _get_contact_phone(data: dict) -> str | None:
    try:
        return data["contacts"]["phone"]
    except TypeError:
        return None


def _build_data(vacancy: dict, exp) -> ResponseVacancy:
    """Getting dataclass object of vacancy data"""
    return ResponseVacancy(
        id=_get_id(vacancy),
        name=_get_name(vacancy),
        company_name=_get_company_name(vacancy),
        experience=exp,
        schedule=_get_schedule(vacancy),
        city=_get_city(vacancy),
        alternate_url=_get_alternate_url(vacancy),
        contact_email=get_contact_email(vacancy),
        contacts_phones=_get_contact_phone(vacancy),
    )


async def _save_vacancies(
    response_vacancies: list[ResponseVacancy], user: User
) -> None:
    for vacancy in response_vacancies:
        _vacancy = await Vacancy.objects.aget_or_create(**vacancy.__dict__)
        await sync_to_async(_vacancy[0].user.add)(user)


async def _parse_vacancies(response_vacancies: dict, exp: str, user: User) -> None:
    vacancies_data = []
    for vacancy in response_vacancies["items"]:
        vacancies_data.append(await sync_to_async(_build_data)(vacancy, exp))
    await _save_vacancies(vacancies_data, user)


def _get_link_to_vacancies(
    exp: str, text: str, page: int = 0, per_page: int = 100
) -> str:
    return LINK_TO_VACANCIES.format(
        experience=exp, text=text, page=page, per_page=per_page
    )


def _create_notification(user: User) -> InfoNotification:
    query = list(
        Vacancy.objects.filter(user=user, vacanciesinfo__is_request=False)[:200]
    )
    notification = Notification.objects.create(user=user)
    notification.vacancies.set(query)
    return InfoNotification(id_notification=notification.pk, count_vacancies=len(query))


async def _get_vacancies(user: User) -> None:
    """get all vacancies."""
    for exp in EXPERIENCE_NAMES:
        response = await _make_request(
            url=_get_link_to_vacancies(exp=exp, text=user.query_text)
        )
        count_page = await _parse_count_page(response)
        for i in range(count_page + 1):
            response_vacancies = await _make_request(
                url=_get_link_to_vacancies(exp=exp, page=i, text=user.query_text)
            )
            await _parse_vacancies(response_vacancies, exp, user)


async def vacancies(user_id) -> None:
    """Getting vacancies from hh, parse and save to Vacancy model,
    then create Notification model and send to telegram message."""
    user = await _get_user(user_id)
    await _get_vacancies(user)
    info_notification = await sync_to_async(_create_notification)(user)
    await main.send_message_notification(info_notification, user)


if __name__ == "__main__":
    pass
