from dataclasses import dataclass
from typing import NoReturn

import aiohttp
from asgiref.sync import sync_to_async

from config.vacancies_settings import (
    ERRORS_TO_CONTINUE,
    ERRORS_TO_BREAK,
    LINK_TO_VACANCY_REQUEST,
)
from models.models import Vacancy, Notification
from user.models import User
from .exceptions import ToContinueError, AuthError, ToBreakError
from .utils import _get_user
from tbot import main

__all__ = ("send_negotiations",)


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


def _update_vacancies_info(model: Vacancy, user) -> None:
    model.vacanciesinfo_set.filter(user=user).update(is_request=True)


def _get_link_to_negotiations(
    vacancy_id: int, resume_id: str, covering_letter: str
) -> str:
    return LINK_TO_VACANCY_REQUEST.format(
        vacancy_id=vacancy_id,
        resume_id=resume_id,
        message=covering_letter,
    )


async def _make_negotiations(
    vacancies_by_notifications: list[Vacancy], user: User, headers: dict
) -> int:
    """
    iteration on list of vacancies and make request to negotiations, then errors check.
    return result of iteration
    """
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
            await sync_to_async(_update_vacancies_info)(vacancy, user)
            count_valid_requests += 1
        except AuthError:
            break
        except ToContinueError:
            await sync_to_async(_update_vacancies_info)(vacancy, user)
        except ToBreakError:
            break
    return count_valid_requests


def _get_vacancies_by_notification(id_notification) -> list[Vacancy]:
    return list(Notification.objects.get(pk=id_notification).vacancies.all())


def _get_headers(user_access_token) -> dict:
    return {"Authorization": f"Bearer {user_access_token}"}


async def send_negotiations(user_id, id_notification: int) -> None:
    """
    Sending negotiations to job post,
    after validation and save to database results (if not errors is_request=True else break)
    and send info message to user, about negotiations.
    """
    user = await _get_user(user_id)
    headers = await sync_to_async(_get_headers)(user.auth_hh.access_token)
    vacancies_to_negotiations = await sync_to_async(_get_vacancies_by_notification)(
        id_notification
    )
    count_valid_negotiations = await _make_negotiations(
        vacancies_to_negotiations, user, headers
    )
    await main.send_info_message_negotiations(
        count_valid_negotiations, user.telegram_id
    )
