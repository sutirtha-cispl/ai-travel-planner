"""Deterministic mock hotel provider (offline, no API keys required)."""

from app.schemas.tools import HotelOption, HotelSearchInput, HotelSearchOutput
from app.tools.base import TravelProvider
from app.tools.mocks.base import stable_seed

# A destination matching this sentinel returns no results.
EMPTY_DESTINATION = "Nowhere"

_HOTEL_NAMES = [
    "The Grand Harbor Hotel",
    "Sunrise Boutique Stay",
    "Royal Continental",
    "The Lakeview Inn",
    "Metropolitan Suites",
    "Casa Verde Residences",
]

_AMENITIES = {
    "wifi",
    "breakfast",
    "gym",
    "pool",
    "spa",
    "parking",
    "airport_shuttle",
    "restaurant",
}


class MockHotelProvider(TravelProvider):
    """Returns stable hotel options derived from the request values."""

    async def execute(self, request: HotelSearchInput) -> HotelSearchOutput:
        if request.destination.strip().lower() == EMPTY_DESTINATION.lower():
            return HotelSearchOutput(
                destination=request.destination,
                check_in=request.check_in,
                check_out=request.check_out,
                options=[],
            )

        seed = stable_seed(f"{request.destination}:{request.check_in}")
        count = 4 + (seed % 3)
        amenities_list = sorted(_AMENITIES)

        options = []
        for index in range(count):
            name = _HOTEL_NAMES[(seed + index) % len(_HOTEL_NAMES)]
            rating = round(3.0 + ((seed + index * 13) % 20) / 10, 1)
            price = float(60 + (seed + index * 41) % 180)
            selected = amenities_list[: 3 + (index % 4)]
            options.append(
                HotelOption(
                    name=name,
                    location=f"{request.destination} city center",
                    rating=rating,
                    room_type="Standard double" if index % 2 == 0 else "Deluxe twin",
                    price_per_night=price,
                    currency="USD",
                    amenities=selected,
                )
            )

        if request.budget_per_night is not None:
            options = [
                option
                for option in options
                if option.price_per_night <= request.budget_per_night
            ]

        return HotelSearchOutput(
            destination=request.destination,
            check_in=request.check_in,
            check_out=request.check_out,
            options=options,
        )
