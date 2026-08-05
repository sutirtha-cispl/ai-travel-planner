"""Trip repository."""

from sqlalchemy.orm import Session

from app.models.trip import Trip
from app.repositories.base_repository import BaseRepository


class TripRepository(BaseRepository[Trip]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Trip)
