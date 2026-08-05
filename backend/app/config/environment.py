"""Environment detection helpers."""

from app.config.settings import settings

ENVIRONMENTS = ("development", "testing", "production")


def current_environment() -> str:
    return settings.APP_ENV if settings.APP_ENV in ENVIRONMENTS else "development"


def is_development() -> bool:
    return current_environment() == "development"


def is_testing() -> bool:
    return current_environment() == "testing"


def is_production() -> bool:
    return current_environment() == "production"
