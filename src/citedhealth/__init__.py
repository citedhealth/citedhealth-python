"""CITED Health — Python client for evidence-based supplement data.

Usage::

    from citedhealth import CitedHealth

    client = CitedHealth()
    evidence = client.get_evidence("biotin", "hair-loss")
    print(f"Grade {evidence.grade}: {evidence.grade_label}")
"""

from citedhealth.client import AsyncCitedHealth, CitedHealth
from citedhealth.exceptions import CitedHealthError, NotFoundError, RateLimitError
from citedhealth.models import (
    Condition,
    EvidenceLink,
    Ingredient,
    NestedIngredient,
    PaginatedResponse,
    Paper,
)

__version__ = "0.3.0"

__all__ = [
    "AsyncCitedHealth",
    "CitedHealth",
    "CitedHealthError",
    "Condition",
    "EvidenceLink",
    "Ingredient",
    "NestedIngredient",
    "NotFoundError",
    "PaginatedResponse",
    "Paper",
    "RateLimitError",
]
