import requests

from .utils import _get_params_for_set_tokens, _get_data_for_update_tokens, _get_headers
from user.models import User, AuthHH
from config.settings import HH_CLIENT_ID, HH_SECRET_KEY
from dataclasses import dataclass


@dataclass
class ResponseToken:
    access_token: str
    refresh_token: str


def get_tokens(headers: dict, data: dict, params: str = "") -> dict:
    return requests.post(
        url=f"https://hh.ru/oauth/token?{params}", headers=headers, data=data
    ).json()


def _update_users_tokens_in_model(user, response) -> None:
    try:
        user.auth_hh.access_token = response["access_token"]
        user.auth_hh.refresh_token = response["refresh_token"]
        user.save()
    except KeyError:
        return None


def _set_users_token_to_model(user, response) -> None:
    # todo Checking for an existing token
    try:
        tokens = AuthHH.objects.create(
            access_token=response["access_token"],
            refresh_token=response["refresh_token"],
        )
        user.auth_hh = tokens
        user.save()
    except KeyError:
        return None


def update_tokens(user: User) -> None:
    """Updates tokens of user hh."""
    data = _get_data_for_update_tokens(user.auth_hh.refresh_token)
    headers = _get_headers()
    response = get_tokens(headers, data)
    _update_users_tokens_in_model(user, response)


def set_user_tokens(user: User, code: str, url: str) -> None:
    """Set new tokens of user hh."""
    headers = _get_headers()
    params = _get_params_for_set_tokens(code, url, HH_CLIENT_ID, HH_SECRET_KEY)
    response = get_tokens(headers, {}, params=params)
    _set_users_token_to_model(user, response)
