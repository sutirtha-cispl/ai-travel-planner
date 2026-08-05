"""Trip endpoints.

Routes only validate requests, call the service layer, and return responses.
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.repositories.trip_repository import TripRepository
from app.schemas.trip import TripCreate, TripResponse
from app.services.trip_service import TripService

router = APIRouter()

DbSession = Annotated[Session, Depends(get_db)]


def get_trip_service(db: DbSession) -> TripService:
    return TripService(TripRepository(db))


TripServiceDependency = Annotated[TripService, Depends(get_trip_service)]


@router.post("/trips", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
def create_trip(
    data: TripCreate,
    service: TripServiceDependency,
) -> TripResponse:
    return TripResponse.model_validate(service.create_trip(data))


@router.get("/trips/{trip_id}", response_model=TripResponse)
def get_trip(
    trip_id: UUID,
    service: TripServiceDependency,
) -> TripResponse:
    trip = service.get_trip(trip_id)
    if trip is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found",
        )
    return TripResponse.model_validate(trip)
