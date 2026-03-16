"""Sync and async HTTP clients for the CITED Health REST API."""

from __future__ import annotations

from typing import Any

import httpx

from citedhealth.exceptions import NotFoundError, RateLimitError
from citedhealth.models import (
    EvidenceLink,
    Ingredient,
    Paper,
)

_DEFAULT_BASE_URL = "https://citedhealth.com"
_DEFAULT_TIMEOUT = 30.0


class CitedHealth:
    """Synchronous client for the CITED Health API.

    Usage::

        client = CitedHealth()
        ingredients = client.search_ingredients("biotin")
        evidence = client.get_evidence("biotin", "hair-loss")
    """

    def __init__(self, base_url: str = _DEFAULT_BASE_URL, timeout: float = _DEFAULT_TIMEOUT) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    def _request(self, path: str, params: dict[str, str] | None = None) -> Any:
        with httpx.Client(timeout=self._timeout) as http:
            resp = http.get(f"{self._base_url}{path}", params=params)

        if resp.status_code == 429:
            retry = int(resp.headers.get("Retry-After", "0"))
            raise RateLimitError(retry_after=retry)
        if resp.status_code == 404:
            raise NotFoundError("resource", path)
        resp.raise_for_status()
        return resp.json()

    def search_ingredients(self, query: str = "", category: str = "") -> list[Ingredient]:
        """Search ingredients by name or category."""
        params: dict[str, str] = {}
        if query:
            params["q"] = query
        if category:
            params["category"] = category
        data = self._request("/api/ingredients/", params=params)
        return [Ingredient.from_dict(item) for item in data.get("results", [])]

    def get_ingredient(self, slug: str) -> Ingredient:
        """Get a single ingredient by slug."""
        data = self._request(f"/api/ingredients/{slug}/")
        return Ingredient.from_dict(data)

    def get_evidence(self, ingredient_slug: str, condition_slug: str) -> EvidenceLink:
        """Get evidence for an ingredient×condition pair."""
        data = self._request(
            "/api/evidence/",
            params={"ingredient": ingredient_slug, "condition": condition_slug},
        )
        results = data.get("results", [])
        if not results:
            raise NotFoundError("evidence", f"{ingredient_slug} × {condition_slug}")
        return EvidenceLink.from_dict(results[0])

    def get_evidence_by_id(self, pk: int) -> EvidenceLink:
        """Get evidence link by primary key."""
        data = self._request(f"/api/evidence/{pk}/")
        return EvidenceLink.from_dict(data)

    def search_papers(self, query: str = "", year: int | None = None) -> list[Paper]:
        """Search PubMed papers by title or year."""
        params: dict[str, str] = {}
        if query:
            params["q"] = query
        if year is not None:
            params["year"] = str(year)
        data = self._request("/api/papers/", params=params)
        return [Paper.from_dict(item) for item in data.get("results", [])]

    def get_paper(self, pmid: str) -> Paper:
        """Get a single paper by PubMed ID."""
        data = self._request(f"/api/papers/{pmid}/")
        return Paper.from_dict(data)


class AsyncCitedHealth:
    """Asynchronous client for the CITED Health API.

    Usage::

        async with AsyncCitedHealth() as client:
            evidence = await client.get_evidence("biotin", "hair-loss")
    """

    def __init__(self, base_url: str = _DEFAULT_BASE_URL, timeout: float = _DEFAULT_TIMEOUT) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._http: httpx.AsyncClient | None = None

    async def __aenter__(self) -> AsyncCitedHealth:
        self._http = httpx.AsyncClient(timeout=self._timeout)
        return self

    async def __aexit__(self, *args: Any) -> None:
        if self._http:
            await self._http.aclose()

    async def _request(self, path: str, params: dict[str, str] | None = None) -> Any:
        if self._http is None:
            self._http = httpx.AsyncClient(timeout=self._timeout)

        resp = await self._http.get(f"{self._base_url}{path}", params=params)

        if resp.status_code == 429:
            retry = int(resp.headers.get("Retry-After", "0"))
            raise RateLimitError(retry_after=retry)
        if resp.status_code == 404:
            raise NotFoundError("resource", path)
        resp.raise_for_status()
        return resp.json()

    async def search_ingredients(self, query: str = "", category: str = "") -> list[Ingredient]:
        params: dict[str, str] = {}
        if query:
            params["q"] = query
        if category:
            params["category"] = category
        data = await self._request("/api/ingredients/", params=params)
        return [Ingredient.from_dict(item) for item in data.get("results", [])]

    async def get_ingredient(self, slug: str) -> Ingredient:
        data = await self._request(f"/api/ingredients/{slug}/")
        return Ingredient.from_dict(data)

    async def get_evidence(self, ingredient_slug: str, condition_slug: str) -> EvidenceLink:
        data = await self._request(
            "/api/evidence/",
            params={"ingredient": ingredient_slug, "condition": condition_slug},
        )
        results = data.get("results", [])
        if not results:
            raise NotFoundError("evidence", f"{ingredient_slug} × {condition_slug}")
        return EvidenceLink.from_dict(results[0])

    async def get_evidence_by_id(self, pk: int) -> EvidenceLink:
        data = await self._request(f"/api/evidence/{pk}/")
        return EvidenceLink.from_dict(data)

    async def search_papers(self, query: str = "", year: int | None = None) -> list[Paper]:
        params: dict[str, str] = {}
        if query:
            params["q"] = query
        if year is not None:
            params["year"] = str(year)
        data = await self._request("/api/papers/", params=params)
        return [Paper.from_dict(item) for item in data.get("results", [])]

    async def get_paper(self, pmid: str) -> Paper:
        data = await self._request(f"/api/papers/{pmid}/")
        return Paper.from_dict(data)
