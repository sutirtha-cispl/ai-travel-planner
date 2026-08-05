"""Trip service: business logic for trips."""

from uuid import UUID

from app.models.trip import Trip
from app.repositories.trip_repository import TripRepository
from app.schemas.trip import TripCreate


class TripService:
    def __init__(self, repository: TripRepository) -> None:
        self.repository = repository

    def create_trip(self, data: TripCreate) -> Trip:
        return self.repository.create(
            destination=data.destination,
            start_date=data.start_date,
            end_date=data.end_date,
        )

    def get_trip(self, trip_id: UUID) -> Trip | None:
        return self.repository.get(trip_id)
