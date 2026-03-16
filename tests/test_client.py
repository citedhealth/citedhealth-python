"""Tests for CitedHealth sync client — mock-based."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from citedhealth import CitedHealth
from citedhealth.exceptions import NotFoundError, RateLimitError
from citedhealth.models import EvidenceLink, Ingredient, Paper


def _mock_response(status_code: int = 200, json_data: Any = None, headers: dict[str, str] | None = None) -> MagicMock:
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = json_data or {}
    resp.headers = headers or {}
    resp.raise_for_status = MagicMock()
    if status_code >= 400:
        resp.raise_for_status.side_effect = Exception(f"HTTP {status_code}")
    return resp


class TestSearchIngredients:
    @patch("citedhealth.client.httpx.Client")
    def test_returns_list_of_ingredients(self, mock_client_cls: MagicMock) -> None:
        mock_client = mock_client_cls.return_value.__enter__.return_value
        mock_client.get.return_value = _mock_response(
            json_data={
                "count": 1,
                "next": None,
                "previous": None,
                "results": [{"id": 1, "name": "Biotin", "slug": "biotin"}],
            }
        )

        client = CitedHealth()
        results = client.search_ingredients("biotin")

        assert len(results) == 1
        assert isinstance(results[0], Ingredient)
        assert results[0].slug == "biotin"

    @patch("citedhealth.client.httpx.Client")
    def test_empty_results(self, mock_client_cls: MagicMock) -> None:
        mock_client = mock_client_cls.return_value.__enter__.return_value
        mock_client.get.return_value = _mock_response(
            json_data={"count": 0, "next": None, "previous": None, "results": []}
        )

        client = CitedHealth()
        results = client.search_ingredients("nonexistent")

        assert results == []


class TestGetIngredient:
    @patch("citedhealth.client.httpx.Client")
    def test_returns_ingredient(self, mock_client_cls: MagicMock) -> None:
        mock_client = mock_client_cls.return_value.__enter__.return_value
        mock_client.get.return_value = _mock_response(
            json_data={"id": 1, "name": "Biotin", "slug": "biotin", "category": "vitamins"}
        )

        client = CitedHealth()
        ing = client.get_ingredient("biotin")

        assert isinstance(ing, Ingredient)
        assert ing.slug == "biotin"

    @patch("citedhealth.client.httpx.Client")
    def test_not_found_raises(self, mock_client_cls: MagicMock) -> None:
        mock_client = mock_client_cls.return_value.__enter__.return_value
        mock_client.get.return_value = _mock_response(status_code=404)

        client = CitedHealth()
        with pytest.raises(NotFoundError):
            client.get_ingredient("nonexistent")


class TestGetEvidence:
    @patch("citedhealth.client.httpx.Client")
    def test_returns_evidence_link(self, mock_client_cls: MagicMock) -> None:
        mock_client = mock_client_cls.return_value.__enter__.return_value
        mock_client.get.return_value = _mock_response(
            json_data={
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 1,
                        "ingredient": {"slug": "biotin", "name": "Biotin"},
                        "condition": {"slug": "hair-loss", "name": "Hair Loss"},
                        "grade": "A",
                        "grade_label": "Strong Evidence",
                        "summary": "Strong support.",
                        "direction": "positive",
                        "total_studies": 12,
                        "total_participants": 1847,
                    }
                ],
            }
        )

        client = CitedHealth()
        ev = client.get_evidence("biotin", "hair-loss")

        assert isinstance(ev, EvidenceLink)
        assert ev.grade == "A"
        assert ev.total_studies == 12

    @patch("citedhealth.client.httpx.Client")
    def test_not_found_raises(self, mock_client_cls: MagicMock) -> None:
        mock_client = mock_client_cls.return_value.__enter__.return_value
        mock_client.get.return_value = _mock_response(
            json_data={"count": 0, "next": None, "previous": None, "results": []}
        )

        client = CitedHealth()
        with pytest.raises(NotFoundError):
            client.get_evidence("nonexistent", "nonexistent")


class TestRateLimiting:
    @patch("citedhealth.client.httpx.Client")
    def test_429_raises_rate_limit_error(self, mock_client_cls: MagicMock) -> None:
        mock_client = mock_client_cls.return_value.__enter__.return_value
        mock_client.get.return_value = _mock_response(status_code=429, headers={"Retry-After": "60"})

        client = CitedHealth()
        with pytest.raises(RateLimitError) as exc_info:
            client.search_ingredients("test")
        assert exc_info.value.retry_after == 60


class TestSearchPapers:
    @patch("citedhealth.client.httpx.Client")
    def test_returns_list_of_papers(self, mock_client_cls: MagicMock) -> None:
        mock_client = mock_client_cls.return_value.__enter__.return_value
        mock_client.get.return_value = _mock_response(
            json_data={
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "pmid": "12345678",
                        "title": "Biotin for Hair",
                        "journal": "J Dermatol",
                        "publication_year": 2024,
                        "study_type": "RCT",
                        "citation_count": 5,
                        "is_open_access": True,
                        "pubmed_link": "https://pubmed.ncbi.nlm.nih.gov/12345678/",
                    }
                ],
            }
        )

        client = CitedHealth()
        results = client.search_papers("biotin")

        assert len(results) == 1
        assert isinstance(results[0], Paper)
        assert results[0].pmid == "12345678"


class TestGetPaper:
    @patch("citedhealth.client.httpx.Client")
    def test_returns_paper(self, mock_client_cls: MagicMock) -> None:
        mock_client = mock_client_cls.return_value.__enter__.return_value
        mock_client.get.return_value = _mock_response(
            json_data={
                "pmid": "12345678",
                "title": "Biotin for Hair",
                "journal": "J Dermatol",
                "publication_year": 2024,
                "study_type": "RCT",
                "citation_count": 5,
                "is_open_access": True,
                "pubmed_link": "https://pubmed.ncbi.nlm.nih.gov/12345678/",
            }
        )

        client = CitedHealth()
        paper = client.get_paper("12345678")

        assert isinstance(paper, Paper)
        assert paper.title == "Biotin for Hair"

    @patch("citedhealth.client.httpx.Client")
    def test_not_found_raises(self, mock_client_cls: MagicMock) -> None:
        mock_client = mock_client_cls.return_value.__enter__.return_value
        mock_client.get.return_value = _mock_response(status_code=404)

        client = CitedHealth()
        with pytest.raises(NotFoundError):
            client.get_paper("99999999")


class TestCustomBaseUrl:
    @patch("citedhealth.client.httpx.Client")
    def test_uses_custom_base_url(self, mock_client_cls: MagicMock) -> None:
        mock_client = mock_client_cls.return_value.__enter__.return_value
        mock_client.get.return_value = _mock_response(
            json_data={"count": 0, "next": None, "previous": None, "results": []}
        )

        client = CitedHealth(base_url="https://haircited.com")
        client.search_ingredients("test")

        call_args = mock_client.get.call_args
        assert "haircited.com" in str(call_args)


class TestAsyncClient:
    @patch("citedhealth.client.httpx.AsyncClient")
    @pytest.mark.anyio
    async def test_search_ingredients(self, mock_client_cls: MagicMock) -> None:
        from citedhealth import AsyncCitedHealth

        mock_instance = mock_client_cls.return_value
        mock_instance.get = AsyncMock(
            return_value=_mock_response(
                json_data={
                    "count": 1,
                    "next": None,
                    "previous": None,
                    "results": [{"id": 1, "name": "Biotin", "slug": "biotin"}],
                }
            )
        )
        mock_instance.aclose = AsyncMock()

        async with AsyncCitedHealth() as client:
            results = await client.search_ingredients("biotin")

        assert len(results) == 1
        assert isinstance(results[0], Ingredient)

    @patch("citedhealth.client.httpx.AsyncClient")
    @pytest.mark.anyio
    async def test_get_evidence(self, mock_client_cls: MagicMock) -> None:
        from citedhealth import AsyncCitedHealth

        mock_instance = mock_client_cls.return_value
        mock_instance.get = AsyncMock(
            return_value=_mock_response(
                json_data={
                    "count": 1,
                    "next": None,
                    "previous": None,
                    "results": [
                        {
                            "id": 1,
                            "ingredient": {"slug": "biotin", "name": "Biotin"},
                            "condition": {"slug": "hair-loss", "name": "Hair Loss"},
                            "grade": "B",
                            "grade_label": "Good Evidence",
                            "summary": "Good support.",
                            "direction": "positive",
                            "total_studies": 5,
                            "total_participants": 300,
                        }
                    ],
                }
            )
        )
        mock_instance.aclose = AsyncMock()

        async with AsyncCitedHealth() as client:
            ev = await client.get_evidence("biotin", "hair-loss")

        assert isinstance(ev, EvidenceLink)
        assert ev.grade == "B"


class TestGetEvidenceById:
    @patch("citedhealth.client.httpx.Client")
    def test_returns_evidence_link(self, mock_client_cls: MagicMock) -> None:
        mock_client = mock_client_cls.return_value.__enter__.return_value
        mock_client.get.return_value = _mock_response(
            json_data={
                "id": 42,
                "ingredient": {"slug": "biotin", "name": "Biotin"},
                "condition": {"slug": "hair-loss", "name": "Hair Loss"},
                "grade": "A",
                "grade_label": "Strong Evidence",
                "summary": "Strong clinical support.",
                "direction": "positive",
                "total_studies": 12,
                "total_participants": 1847,
            }
        )

        client = CitedHealth()
        ev = client.get_evidence_by_id(42)

        assert isinstance(ev, EvidenceLink)
        assert ev.id == 42
        assert ev.grade == "A"
        assert ev.ingredient.slug == "biotin"

    @patch("citedhealth.client.httpx.Client")
    def test_raises_not_found(self, mock_client_cls: MagicMock) -> None:
        mock_client = mock_client_cls.return_value.__enter__.return_value
        mock_client.get.return_value = _mock_response(status_code=404)

        client = CitedHealth()
        with pytest.raises(NotFoundError):
            client.get_evidence_by_id(99999)
