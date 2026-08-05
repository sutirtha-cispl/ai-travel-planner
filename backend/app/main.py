"""Application entry point.

Creates the FastAPI application, registers middleware and API routes.
Contains no business logic, AI logic, or database queries.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import chat, health, trips
from app.config.settings import settings
from app.core.logging import setup_logging
from app.middleware.logging import RequestLoggingMiddleware

setup_logging()


def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        docs_url="/docs",
        openapi_url="/openapi.json",
    )

    application.add_middleware(RequestLoggingMiddleware)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(health.router, prefix=settings.API_V1_PREFIX)
    application.include_router(chat.router, prefix=settings.API_V1_PREFIX)
    application.include_router(trips.router, prefix=settings.API_V1_PREFIX)

    @application.get("/", tags=["meta"])
    def root() -> dict[str, str]:
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "docs": "/docs",
        }

    return application


app = create_app()
