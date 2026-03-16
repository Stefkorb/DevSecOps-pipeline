from fastapi import FastAPI

from app.routes.health import router as health_router
from app.routes.info import router as info_router
from app.routes.protected import router as protected_router

app = FastAPI(
    title="Enterprise DevSecOps Demo API",
    description=(
        "A small containerized web application used to demonstrate "
        "an enterprise-style DevSecOps pipeline."
    ),
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(info_router)
app.include_router(protected_router)
