"""Deterministic mock currency provider (offline, no API keys required)."""

import logging

from app.schemas.tools import (
    CurrencyConversionInput,
    CurrencyConversionOutput,
)
from app.tools.base import TravelProvider

logger = logging.getLogger(__name__)

# Fixed reference rates (1 unit of each currency expressed in USD terms is
# derived by converting through this base table). Kept deterministic for tests.
_EXCHANGE_RATES: dict[str, float] = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.78,
    "JPY": 151.0,
    "INR": 83.5,
    "CNY": 7.2,
    "KRW": 1360.0,
    "AUD": 1.52,
    "CAD": 1.36,
    "SGD": 1.34,
    "THB": 36.5,
    "AED": 3.67,
    "CHF": 0.88,
    "HKD": 7.82,
    "NZD": 1.66,
    "MXN": 17.2,
    "BRL": 5.1,
    "ZAR": 18.4,
    "IDR": 15800.0,
    "MYR": 4.7,
    "PHP": 56.0,
    "VND": 24500.0,
}

_DEFAULT_RATE = 1.0


class MockCurrencyProvider(TravelProvider):
    """Converts amounts using a fixed, deterministic rate table."""

    async def execute(
        self, request: CurrencyConversionInput
    ) -> CurrencyConversionOutput:
        source_rate = _rate(request.source)
        target_rate = _rate(request.target)
        exchange_rate = round(target_rate / source_rate, 6)
        converted = round(request.amount * exchange_rate, 2)

        return CurrencyConversionOutput(
            source=request.source,
            target=request.target,
            amount=request.amount,
            exchange_rate=exchange_rate,
            converted_amount=converted,
        )


def _rate(currency: str) -> float:
    rate = _EXCHANGE_RATES.get(currency)
    if rate is None:
        logger.warning(
            "No mock exchange rate for '%s'; defaulting to 1.0", currency
        )
        return _DEFAULT_RATE
    return rate
