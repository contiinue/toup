import aiohttp
import asyncio

from config.hh_settings import EXPERIENCE_NAMES, LINK_TO_VACANCIES, QUERY_HH
from dataclasses import dataclass

from models.models import Vacancy


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


async def _auth():
    async with aiohttp.ClientSession() as session:
        async with session.post(url="", data={}) as response:
            return await response.json()


async def _make_request(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as response:
            return await response.json()


async def _parse_count_page(data: dict) -> int:
    return data["pages"]


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


async def _save_vacancies(vacancies: list[ResponseVacancy]) -> None:
    for vacancy in vacancies:
        await Vacancy.objects.aget_or_create(**vacancy.__dict__)


async def _parse_vacancies(vacancies: dict, exp: str) -> None:
    vacancies_data = []
    for vacancy in vacancies["items"]:
        vacancies_data.append(_build_data(vacancy, exp))
    await _save_vacancies(vacancies_data)


def _get_url(exp: str, page: int = 0, per_page: int = 100) -> str:
    return LINK_TO_VACANCIES.format(
        experience=exp, text=QUERY_HH, page=page, per_page=per_page
    )


async def _get_vacancies() -> None:
    """get all vacancies."""
    for exp in EXPERIENCE_NAMES:
        response = await _make_request(url=_get_url(exp=exp))
        count_page = await _parse_count_page(response)
        for i in range(count_page + 1):
            vacancies = await _make_request(url=_get_url(exp=exp, page=i))
            await _parse_vacancies(vacancies, exp)


async def get_vacancies():
    await _get_vacancies()


async def make_mailings():
    pass


if __name__ == "__main__":
    asyncio.run(get_vacancies())
