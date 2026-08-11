"""Unit tests for the chat result formatter."""

from app.services.chat_service import (
    FAILED_RESPONSE,
    RATE_LIMITED_RESPONSE,
    _activity_emoji,
    _format_budget,
    _format_date,
    _is_rate_limit_error,
    format_result,
)

BASE_ITINERARY = {
    "destination": "Goa",
    "duration": 7,
    "days": [
        {
            "day": 1,
            "title": "Beach Day",
            "activities": [
                {
                    "time": "09:00",
                    "name": "Relax on the beach",
                    "description": "Soak up the sun",
                    "category": "beach",
                    "estimated_cost": 50,
                },
                {
                    "time": "14:00",
                    "name": "Water sports",
                    "category": "water",
                    "description": "",
                    "estimated_cost": None,
                },
            ],
            "notes": "Pack sunscreen.",
        }
    ],
    "summary": "A relaxing week in Goa.",
}


def test_format_result_header_includes_trip_details():
    result = {
        "destination": "Goa",
        "origin": "Kolkata",
        "travel_dates": {"start": "2026-10-01", "end": "2026-10-07"},
        "travelers": 2,
        "budget": 2000,
        "itinerary": BASE_ITINERARY,
    }

    output = format_result(result)

    assert "## 🗺️ Your Trip to Goa" in output
    assert "📍 **From:** Kolkata → Goa" in output
    assert "📅 **Dates:** **Oct 01, 2026** – **Oct 07, 2026**" in output
    assert "👥 **Travelers:** 2 adults" in output
    assert "💰 **Budget:** $2,000" in output


def test_format_result_builds_emoji_day_sections():
    result = {"itinerary": BASE_ITINERARY}

    output = format_result(result)

    assert "### 📅 Day 1 — Beach Day" in output
    assert "- 🕘 09:00 · 🏖️ **Relax on the beach** — Soak up the sun (💵 $50)" in output
    assert "- 🕘 14:00 · 🌊 **Water sports**" in output
    assert "📝 *Pack sunscreen.*" in output


def test_format_result_appends_summary():
    output = format_result({"itinerary": BASE_ITINERARY})

    assert "### ✨ Summary" in output
    assert "A relaxing week in Goa." in output


def test_format_result_falls_back_when_details_missing():
    result = {
        "itinerary": {
            "destination": None,
            "duration": None,
            "days": [{"day": 1, "title": "", "activities": [], "notes": ""}],
            "summary": "",
        }
    }

    output = format_result(result)

    assert "## 🗺️ Your Trip" in output
    assert "### 📅 Day 1" in output
    assert "- Free time" in output


def test_format_result_returns_final_response_when_set():
    output = format_result({"final_response": "Please share your destination."})

    assert output == "Please share your destination."


def test_format_result_returns_failed_response_on_failure():
    output = format_result({"status": "failed", "error": "boom"})

    assert output == FAILED_RESPONSE


def test_format_result_returns_rate_limited_response_on_429():
    output = format_result(
        {
            "status": "failed",
            "error": "supervisor failed: Error code: 429 - rate_limit_exceeded",
        }
    )

    assert output == RATE_LIMITED_RESPONSE
    assert output != FAILED_RESPONSE


def test_is_rate_limit_error_detects_provider_errors():
    assert _is_rate_limit_error("Error code: 429 - rate_limit_exceeded")
    assert _is_rate_limit_error("Rate limit reached for model")
    assert _is_rate_limit_error("supervisor failed: Error code: 429 - ...")
    assert not _is_rate_limit_error("connection reset")
    assert not _is_rate_limit_error("")


def test_format_result_returns_fallback_without_itinerary():
    output = format_result({})

    assert output == "I don't have enough information to create a plan yet."


def test_format_budget_uses_thousands_separator():
    assert _format_budget(2000) == "$2,000"
    assert _format_budget(1) == "$1"
    assert _format_budget(None) == ""


def test_format_date_reads_iso_dates():
    assert _format_date("2026-10-01") == "Oct 01, 2026"
    assert _format_date("not-a-date") == "not-a-date"


def test_activity_emoji_matches_categories():
    assert _activity_emoji("beach and sun") == "🏖️"
    assert _activity_emoji("Museum tour") == "🏛️"
    assert _activity_emoji("cooking class") == "👨‍🍳"
    assert _activity_emoji("unknown") == "📍"
