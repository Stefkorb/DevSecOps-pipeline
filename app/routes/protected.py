from fastapi import APIRouter, Header, HTTPException, status

from app.services.auth_service import is_token_valid

router = APIRouter(tags=["protected"])


@router.get("/auth/check")
def auth_check(x_api_token: str | None = Header(default=None)) -> dict:
    if not is_token_valid(x_api_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API token.",
        )

    return {"message": "Token is valid."}


@router.get("/protected")
def protected_endpoint(x_api_token: str | None = Header(default=None)) -> dict:
    if not is_token_valid(x_api_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access denied.",
        )

    return {
        "message": "You have access to the protected endpoint.",
        "security": "token-validated",
    }
