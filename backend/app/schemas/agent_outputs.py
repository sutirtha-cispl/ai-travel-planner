"""Structured output schemas for AI agents.

Each agent produces one of these validated Pydantic objects. This guarantees
that downstream agents and the API only ever receive schema-valid data.
"""

from pydantic import BaseModel, Field


class RequirementOutput(BaseModel):
    """Structured requirements extracted from the user's message."""

    destination: str | None = None
    origin: str | None = None
    travel_dates: dict[str, str] | None = None
    duration: int | None = None
    travelers: int | None = None
    budget: int | None = None
    preferences: list[str] = Field(default_factory=list)
    missing_fields: list[str] = Field(default_factory=list)


class SupervisorDecision(BaseModel):
    """Workflow decision produced by the supervisor agent."""

    next_step: str = Field(
        ...,
        description="One of: planner, itinerary, review, ask_user, end",
    )
    reason: str = Field(
        default="",
        description="Short justification for the decision",
    )


class PlannerOutput(BaseModel):
    """High-level travel strategy produced by the planner agent."""

    strategy: str
    focus_areas: list[str] = Field(default_factory=list)
    estimated_budget: int | None = None


class Activity(BaseModel):
    """A single scheduled activity inside a day plan."""

    time: str | None = None
    name: str
    description: str = ""
    category: str = ""
    estimated_cost: int | None = None


class DayPlan(BaseModel):
    """One day of the itinerary."""

    day: int
    title: str = ""
    activities: list[Activity] = Field(default_factory=list)
    notes: str = ""


class ItineraryOutput(BaseModel):
    """Final day-by-day itinerary produced by the itinerary agent."""

    days: list[DayPlan] = Field(default_factory=list)
    summary: str = ""


class ReviewNote(BaseModel):
    """Single quality note produced by the review agent."""

    severity: str = Field(..., description="One of: error, warning, info")
    message: str


class ReviewOutput(BaseModel):
    """Validation result produced by the review agent."""

    approved: bool
    issues: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    review_notes: list[ReviewNote] = Field(default_factory=list)
