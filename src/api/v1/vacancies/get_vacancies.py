import aiohttp

from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist

from config.vacancies_settings import (
    EXPERIENCE_NAMES,
    LINK_TO_VACANCIES,
    LINK_TO_VACANCY_REQUEST,
    ERRORS_TO_BREAK,
    ERRORS_TO_CONTINUE,
)
from dataclasses import dataclass
from models.models import Vacancy, Notification
from tbot import main
from user.models import User

from .exceptions import AuthError, ToContinueError, ToBreakError
from typing import NoReturn

__all__ = ("vacancies", "send_negotiations")


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


@dataclass
class SendOutResumeResponse:
    status_code: int
    response_json: dict


async def _make_request_to_negotiations(url, headers) -> SendOutResumeResponse:
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, headers=headers) as response:
            return SendOutResumeResponse(
                status_code=response.status,
                response_json=await response.json() if response.status != 201 else None,
            )


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
        await Vacancy.objects.aget_or_create(user=user, **vacancy.__dict__)


async def _parse_vacancies(response_vacancies: dict, exp: str, user: User) -> None:
    vacancies_data = []
    for vacancy in response_vacancies["items"]:
        vacancies_data.append(_build_data(vacancy, exp))
    await _save_vacancies(vacancies_data, user)


def _get_link_to_vacancies(
    exp: str, text: str, page: int = 0, per_page: int = 100
) -> str:
    return LINK_TO_VACANCIES.format(
        experience=exp, text=text, page=page, per_page=per_page
    )


def _create_notification(user: User) -> InfoNotification:
    query = list(Vacancy.objects.filter(is_request=False, user=user)[:200])
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


def _check_response_negotiations(response: SendOutResumeResponse) -> NoReturn | None:
    try:
        if response.status_code != 201 and response.response_json is not None:
            if response.response_json["errors"][0]["value"] in ERRORS_TO_CONTINUE:
                raise ToContinueError
            elif response.response_json["errors"][0]["value"] in ERRORS_TO_BREAK:
                raise ToBreakError
            else:
                raise AuthError
    except KeyError:
        return ToContinueError


def _get_link_to_negotiations(
    vacancy_id: int, resume_id: str, covering_letter: str
) -> str:
    return LINK_TO_VACANCY_REQUEST.format(
        vacancy_id=vacancy_id,
        resume_id=resume_id,
        message=covering_letter,
    )


async def _get_user(user_id) -> User | None:
    try:
        return await sync_to_async(User.objects.get)(pk=user_id)
    except ObjectDoesNotExist:
        return None


def _get_headers(user_access_token) -> dict:
    return {"Authorization": f"Bearer {user_access_token}"}


def _get_notification(id_notification) -> list[Vacancy]:
    return list(Notification.objects.get(pk=id_notification).vacancies.all())


async def _make_negotiations(
    vacancies_by_notifications: list[Vacancy], user: User, headers: dict
) -> int:
    count_valid_requests = 0
    for vacancy in vacancies_by_notifications:
        response = await _make_request_to_negotiations(
            url=_get_link_to_negotiations(
                vacancy.pk, user.resume_id, user.covering_letter
            ),
            headers=headers,
        )
        try:
            await sync_to_async(_check_response_negotiations)(response)
            count_valid_requests += 1
        except AuthError:
            break
        except ToContinueError:
            continue
        except ToBreakError:
            break
    return count_valid_requests


async def vacancies(user_id) -> None:
    """Getting vacancies from hh, parse and save to Vacancy model,
    then create Notification model and send to telegram message."""
    user = await _get_user(user_id)
    await _get_vacancies(user)
    info_notification = await sync_to_async(_create_notification)(user)
    await main.send_message_notification(info_notification, user)


async def send_negotiations(user_id, id_notification: int) -> None:
    user = await _get_user(user_id)
    headers = await sync_to_async(_get_headers)(user.auth_hh.access_token)
    vacancies_to_negotiations = await sync_to_async(_get_notification)(id_notification)
    count_valid_negotiations = await _make_negotiations(
        vacancies_to_negotiations, user, headers
    )


if __name__ == "__main__":
    pass
