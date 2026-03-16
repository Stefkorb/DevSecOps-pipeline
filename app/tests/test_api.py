from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# Normal /health endpoint behaviour check
def test_health_endpoint_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "enterprise-devsecops-demo-api"


# Normal /info endpoint behaviour check
def test_info_endpoint_returns_expected_config() -> None:
    response = client.get("/info")

    assert response.status_code == 200
    body = response.json()

    assert body["app_name"] == "DevSecOps Demo API"
    assert "environment" in body
    assert "feature_flag_demo" in body
    assert "app_port" in body


# basic /auth/check endpoint unauthorized behaviour
def test_auth_check_without_token_returns_401() -> None:
    response = client.get("/auth/check")

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or missing API token."


# basic /protected endpoint unauthorized behaviour
def test_protected_endpoint_without_token_returns_401() -> None:
    response = client.get("/protected")

    assert response.status_code == 401
    assert response.json()["detail"] == "Access denied."


# basic /auth/check endpoint token validation behaviour
def test_auth_check_with_valid_token_returns_200() -> None:
    response = client.get("/auth/check", headers={"x-api-token": "changeme"})

    assert response.status_code == 200
    assert response.json()["message"] == "Token is valid."


# basic /protected endpoint authorized behaviour
def test_protected_endpoint_with_valid_token_returns_200() -> None:
    response = client.get("/protected", headers={"x-api-token": "changeme"})

    assert response.status_code == 200
    body = response.json()

    assert body["message"] == "You have access to the protected endpoint."
    assert body["security"] == "token-validated"
