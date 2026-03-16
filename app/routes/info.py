from fastapi import APIRouter

from app.config import get_app_env, get_app_port, get_feature_flag_demo

router = APIRouter(tags=["info"])


@router.get("/info")
def app_info() -> dict:
    return {
        "app_name": "DevSecOps Demo API",
        "environment": get_app_env(),
        "feature_flag_demo": get_feature_flag_demo(),
        "app_port": get_app_port(),
    }
