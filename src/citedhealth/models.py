"""Data models for CITED Health API responses.

All models are frozen dataclasses with a ``from_dict()`` class method
for parsing JSON response dicts from the REST API.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Ingredient:
    """A supplement ingredient."""

    id: int
    name: str
    slug: str
    category: str = ""
    mechanism: str = ""
    recommended_dosage: dict[str, str] = field(default_factory=dict)
    forms: list[str] = field(default_factory=list)
    is_featured: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Ingredient:
        return cls(
            id=data.get("id", 0),
            name=data.get("name", ""),
            slug=data.get("slug", ""),
            category=data.get("category", ""),
            mechanism=data.get("mechanism", ""),
            recommended_dosage=data.get("recommended_dosage", {}),
            forms=data.get("forms", []),
            is_featured=data.get("is_featured", False),
        )


@dataclass(frozen=True)
class Condition:
    """A health condition (nested in EvidenceLink)."""

    slug: str
    name: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Condition:
        return cls(slug=data.get("slug", ""), name=data.get("name", ""))


@dataclass(frozen=True)
class Paper:
    """A PubMed-indexed paper."""

    id: int
    pmid: str
    title: str
    journal: str
    publication_year: int | None = None
    study_type: str = ""
    citation_count: int = 0
    is_open_access: bool = False
    pubmed_link: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Paper:
        return cls(
            id=data.get("id", 0),
            pmid=data.get("pmid", ""),
            title=data.get("title", ""),
            journal=data.get("journal", ""),
            publication_year=data.get("publication_year"),
            study_type=data.get("study_type", ""),
            citation_count=data.get("citation_count", 0),
            is_open_access=data.get("is_open_access", False),
            pubmed_link=data.get("pubmed_link", ""),
        )


@dataclass(frozen=True)
class NestedIngredient:
    """Nested ingredient reference — API returns {slug, name} only."""

    slug: str = ""
    name: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> NestedIngredient:
        return cls(slug=data.get("slug", ""), name=data.get("name", ""))


@dataclass(frozen=True)
class EvidenceLink:
    """Evidence for an ingredient×condition pair."""

    id: int
    ingredient: NestedIngredient
    condition: Condition
    grade: str
    grade_label: str = ""
    summary: str = ""
    direction: str = ""
    total_studies: int = 0
    total_participants: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EvidenceLink:
        return cls(
            id=data.get("id", 0),
            ingredient=NestedIngredient.from_dict(data.get("ingredient", {})),
            condition=Condition.from_dict(data.get("condition", {})),
            grade=data.get("grade", ""),
            grade_label=data.get("grade_label", ""),
            summary=data.get("summary", ""),
            direction=data.get("direction", ""),
            total_studies=data.get("total_studies", 0),
            total_participants=data.get("total_participants", 0),
        )


@dataclass(frozen=True)
class PaginatedResponse:
    """Paginated API response wrapper."""

    count: int
    next: str | None
    previous: str | None
    results: list[Any]

    @classmethod
    def from_dict(cls, data: dict[str, Any], model_cls: type[T]) -> PaginatedResponse:
        return cls(
            count=data.get("count", 0),
            next=data.get("next"),
            previous=data.get("previous"),
            results=[model_cls.from_dict(item) for item in data.get("results", [])],  # type: ignore[attr-defined]
        )
