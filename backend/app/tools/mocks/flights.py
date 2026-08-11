"""Deterministic mock flight provider (offline, no API keys required)."""

from app.schemas.tools import (
    CabinClass,
    FlightOption,
    FlightSearchInput,
    FlightSearchOutput,
)
from app.tools.base import TravelProvider
from app.tools.mocks.base import stable_seed

# A destination matching this sentinel returns no results. Useful for testing
# the empty-result path without hitting a real API.
EMPTY_DESTINATION = "Nowhere"

_AIRLINES = [
    ("Skyline Air", "SK"),
    ("Pacific Wings", "PW"),
    ("Everest Airlines", "EA"),
    ("Horizon Air", "HA"),
    ("Blue Jet", "BJ"),
]

_CABIN_MULTIPLIER = {
    CabinClass.economy: 1.0,
    CabinClass.premium_economy: 1.4,
    CabinClass.business: 2.6,
    CabinClass.first: 4.0,
}


class MockFlightProvider(TravelProvider):
    """Returns stable flight options derived from the request values."""

    async def execute(self, request: FlightSearchInput) -> FlightSearchOutput:
        if request.destination.strip().lower() == EMPTY_DESTINATION.lower():
            return FlightSearchOutput(
                origin=request.origin,
                destination=request.destination,
                departure_date=request.departure_date,
                options=[],
            )

        seed = stable_seed(
            f"{request.origin}:{request.destination}:{request.departure_date}"
        )
        multiplier = _CABIN_MULTIPLIER[request.cabin_class]
        base_price = (220.0 + (seed % 800)) * multiplier
        base_duration = 300 + (seed % 600)
        count = 3 + (seed % 2)

        options = []
        for index in range(count):
            airline, code = _AIRLINES[index % len(_AIRLINES)]
            number = 100 + (seed + index * 37) % 900
            departure_minutes = 6 * 60 + (seed + index * 97) % (12 * 60)
            duration_minutes = base_duration + index * 15
            arrival_minutes = (departure_minutes + duration_minutes) % (24 * 60)
            departure_hours, departure_mins = divmod(
                departure_minutes, 60
            )
            arrival_hours, arrival_mins = divmod(arrival_minutes, 60)
            options.append(
                FlightOption(
                    airline=airline,
                    flight_number=f"{code}{number}",
                    departure=f"{departure_hours:02d}:{departure_mins:02d}",
                    arrival=f"{arrival_hours:02d}:{arrival_mins:02d}",
                    duration_minutes=duration_minutes,
                    price=round(base_price + index * 35, 2),
                    currency="USD",
                )
            )

        return FlightSearchOutput(
            origin=request.origin,
            destination=request.destination,
            departure_date=request.departure_date,
            options=options,
        )
