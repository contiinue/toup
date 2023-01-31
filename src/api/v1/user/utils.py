def get_url_to_grant_access(hh_client_id, redirect_url):
    return (
        f"https://hh.ru/oauth/authorize?"
        f"response_type=code&"
        f"client_id={hh_client_id}&"
        f"redirect_uri={redirect_url}"
    )


def _get_params_for_set_tokens(
    code: str, url: str, hh_client_id: str, hh_secret_key: str
) -> str:
    return (
        f"grant_type=authorization_code&"
        f"client_id={hh_client_id}&"
        f"client_secret={hh_secret_key}&"
        f"code={code}&"
        f"redirect_uri={url}"
    )


def _get_headers() -> dict:
    return {"Content-Type": "application/x-www-form-urlencoded"}


def _get_data_for_update_tokens(refresh_token: str) -> dict:
    return {"grant_type": "refresh_token", "refresh_token": refresh_token}
