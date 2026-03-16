from app.config import get_auth_token


def is_token_valid(token: str | None) -> bool:
    expected_token = get_auth_token()

    if not token:
        return False

    return token == expected_token
