"""Tests for data models — parsing from API JSON responses."""

from __future__ import annotations

from citedhealth.models import (
    EvidenceLink,
    Ingredient,
    PaginatedResponse,
    Paper,
)


class TestIngredientModel:
    def test_from_dict(self) -> None:
        data = {
            "id": 1,
            "name": "Biotin",
            "slug": "biotin",
            "category": "vitamins",
            "mechanism": "Supports keratin synthesis",
            "recommended_dosage": {"general": "30-100 mcg"},
            "forms": ["capsule", "powder"],
            "is_featured": True,
        }
        ing = Ingredient.from_dict(data)
        assert ing.name == "Biotin"
        assert ing.slug == "biotin"
        assert ing.category == "vitamins"
        assert ing.is_featured is True
        assert ing.forms == ["capsule", "powder"]

    def test_from_dict_missing_optional_fields(self) -> None:
        data = {"id": 1, "name": "Biotin", "slug": "biotin"}
        ing = Ingredient.from_dict(data)
        assert ing.category == ""
        assert ing.mechanism == ""
        assert ing.forms == []


class TestPaperModel:
    def test_from_dict(self) -> None:
        data = {
            "id": 1,
            "pmid": "12345678",
            "title": "Biotin and Hair Growth",
            "journal": "J Dermatology",
            "publication_year": 2024,
            "study_type": "Randomized Controlled Trial",
            "citation_count": 42,
            "is_open_access": True,
            "pubmed_link": "https://pubmed.ncbi.nlm.nih.gov/12345678/",
        }
        paper = Paper.from_dict(data)
        assert paper.pmid == "12345678"
        assert paper.citation_count == 42
        assert paper.pubmed_link == "https://pubmed.ncbi.nlm.nih.gov/12345678/"


class TestEvidenceLinkModel:
    def test_from_dict(self) -> None:
        data = {
            "id": 1,
            "ingredient": {"slug": "biotin", "name": "Biotin"},
            "condition": {"slug": "hair-loss", "name": "Hair Loss"},
            "grade": "A",
            "grade_label": "Strong Evidence",
            "summary": "Strong clinical support.",
            "direction": "positive",
            "total_studies": 12,
            "total_participants": 1847,
        }
        ev = EvidenceLink.from_dict(data)
        assert ev.grade == "A"
        assert ev.ingredient.slug == "biotin"
        assert ev.condition.name == "Hair Loss"
        assert ev.total_studies == 12


class TestPaginatedResponse:
    def test_from_dict_with_ingredients(self) -> None:
        data = {
            "count": 2,
            "next": "https://citedhealth.com/api/ingredients/?page=2",
            "previous": None,
            "results": [
                {"id": 1, "name": "Biotin", "slug": "biotin"},
                {"id": 2, "name": "Iron", "slug": "iron"},
            ],
        }
        page = PaginatedResponse.from_dict(data, Ingredient)
        assert page.count == 2
        assert page.next == "https://citedhealth.com/api/ingredients/?page=2"
        assert page.previous is None
        assert len(page.results) == 2
        assert isinstance(page.results[0], Ingredient)
