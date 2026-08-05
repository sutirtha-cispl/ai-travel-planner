"""Database engine creation."""

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.config.settings import settings


def _build_engine() -> Engine:
    connect_args: dict[str, object] = {}
    if settings.DATABASE_URL.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    return create_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        connect_args=connect_args,
    )


engine = _build_engine()
