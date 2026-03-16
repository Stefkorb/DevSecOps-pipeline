import os


def get_app_env() -> str:
    return os.getenv("APP_ENV", "development")


def get_app_port() -> str:
    return os.getenv("APP_PORT", "8000")


def get_feature_flag_demo() -> str:
    return os.getenv("FEATURE_FLAG_DEMO", "false")


def get_auth_token() -> str:
    return os.getenv("AUTH_TOKEN", "changeme")
