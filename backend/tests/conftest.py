"""Test fixtures and application-wide test configuration."""

import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

os.environ.setdefault("APP_ENV", "testing")
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_travel.db")


@pytest.fixture(scope="session", autouse=True)
def setup_database() -> None:
    from app import models  # noqa: F401
    from app.database.base import Base
    from app.database.connection import engine

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@pytest.fixture()
def client() -> TestClient:
    from app.main import app

    with TestClient(app) as test_client:
        yield test_client
