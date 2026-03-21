"""Command-line interface for citedhealth.

Requires the ``cli`` extra: ``pip install citedhealth[cli]``

Usage::

    citedhealth ingredients biotin
    citedhealth ingredient biotin
    citedhealth evidence biotin hair-loss
    citedhealth papers --year 2024
    citedhealth paper 12345678
"""

from __future__ import annotations

import dataclasses
import json
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from citedhealth.client import CitedHealth

app = typer.Typer(
    name="citedhealth",
    help="Evidence-based supplement research — search ingredients, evidence grades, and PubMed papers.",
    no_args_is_help=True,
)
console = Console()

_GRADE_STYLE: dict[str, str] = {
    "A": "green",
    "B": "blue",
    "C": "yellow",
    "D": "dim",
    "F": "red",
}


def _grade_markup(grade: str) -> str:
    """Return Rich markup for an evidence grade letter."""
    style = _GRADE_STYLE.get(grade, "")
    return f"[{style}]{grade}[/{style}]" if style else grade


def _version_callback(value: bool) -> None:  # noqa: FBT001
    if value:
        import importlib.metadata

        version = importlib.metadata.version("citedhealth")
        console.print(f"citedhealth {version}")
        raise typer.Exit


@app.callback()
def main(
    version: Annotated[
        bool | None,
        typer.Option("--version", "-v", callback=_version_callback, is_eager=True, help="Show version and exit."),
    ] = None,
) -> None:
    """Evidence-based supplement research — search ingredients, evidence grades, and PubMed papers."""


@app.command()
def ingredients(
    query: Annotated[str, typer.Argument(help="Search query (ingredient name or keyword)")] = "",
    category: Annotated[str | None, typer.Option("--category", "-c", help="Filter by category")] = None,
    as_json: Annotated[bool, typer.Option("--json", help="Output as compact JSON")] = False,
) -> None:
    """Search supplement ingredients by name or keyword."""
    client = CitedHealth()
    results = client.search_ingredients(query=query, category=category or "")

    if as_json:
        print(json.dumps([dataclasses.asdict(r) for r in results]))  # noqa: T201
        return

    if not results:
        console.print("[yellow]No ingredients found.[/yellow]")
        return

    table = Table(title="Ingredients")
    table.add_column("Name", style="cyan")
    table.add_column("Slug")
    table.add_column("Category")
    table.add_column("Featured", justify="center")

    for item in results:
        table.add_row(
            item.name,
            item.slug,
            item.category,
            "Y" if item.is_featured else "",
        )

    console.print(table)
    console.print(f"[dim]{len(results)} result(s)[/dim]")


@app.command()
def ingredient(
    slug: Annotated[str, typer.Argument(help="Ingredient slug (e.g. 'biotin')")],
    as_json: Annotated[bool, typer.Option("--json", help="Output as compact JSON")] = False,
) -> None:
    """Get a single ingredient by slug."""
    client = CitedHealth()
    item = client.get_ingredient(slug)

    if as_json:
        print(json.dumps(dataclasses.asdict(item)))  # noqa: T201
        return

    table = Table(title=f"Ingredient: {item.name}")
    table.add_column("Property", style="cyan")
    table.add_column("Value")

    table.add_row("Name", item.name)
    table.add_row("Slug", item.slug)
    table.add_row("Category", item.category)
    table.add_row("Mechanism", item.mechanism or "[dim]—[/dim]")
    table.add_row("Dosage", json.dumps(item.recommended_dosage) if item.recommended_dosage else "[dim]—[/dim]")
    table.add_row("Forms", ", ".join(item.forms) if item.forms else "[dim]—[/dim]")
    table.add_row("Featured", "Yes" if item.is_featured else "No")

    console.print(table)


@app.command()
def evidence(
    ingredient_slug: Annotated[str, typer.Argument(help="Ingredient slug (e.g. 'biotin')")],
    condition_slug: Annotated[str, typer.Argument(help="Condition slug (e.g. 'hair-loss')")],
    as_json: Annotated[bool, typer.Option("--json", help="Output as compact JSON")] = False,
) -> None:
    """Get evidence grade for an ingredient-condition pair."""
    client = CitedHealth()
    ev = client.get_evidence(ingredient_slug, condition_slug)

    if as_json:
        print(json.dumps(dataclasses.asdict(ev)))  # noqa: T201
        return

    table = Table(title=f"Evidence: {ev.ingredient.name} for {ev.condition.name}")
    table.add_column("Property", style="cyan")
    table.add_column("Value")

    table.add_row("Grade", _grade_markup(ev.grade))
    table.add_row("Label", ev.grade_label)
    table.add_row("Direction", ev.direction or "[dim]—[/dim]")
    table.add_row("Summary", ev.summary or "[dim]—[/dim]")
    table.add_row("Studies", str(ev.total_studies))
    table.add_row("Participants", str(ev.total_participants))

    console.print(table)


@app.command()
def papers(
    query: Annotated[str, typer.Argument(help="Search query (paper title keyword)")] = "",
    year: Annotated[int | None, typer.Option("--year", "-y", help="Filter by publication year")] = None,
    as_json: Annotated[bool, typer.Option("--json", help="Output as compact JSON")] = False,
) -> None:
    """Search PubMed-indexed papers."""
    client = CitedHealth()
    results = client.search_papers(query=query, year=year)

    if as_json:
        print(json.dumps([dataclasses.asdict(r) for r in results]))  # noqa: T201
        return

    if not results:
        console.print("[yellow]No papers found.[/yellow]")
        return

    table = Table(title="Papers")
    table.add_column("PMID", style="dim")
    table.add_column("Title", max_width=60)
    table.add_column("Year", justify="center")
    table.add_column("Type")
    table.add_column("Citations", justify="right")

    for item in results:
        table.add_row(
            item.pmid,
            item.title[:60],
            str(item.publication_year or ""),
            item.study_type,
            str(item.citation_count),
        )

    console.print(table)
    console.print(f"[dim]{len(results)} result(s)[/dim]")


@app.command()
def paper(
    pmid: Annotated[str, typer.Argument(help="PubMed ID")],
    as_json: Annotated[bool, typer.Option("--json", help="Output as compact JSON")] = False,
) -> None:
    """Get a single paper by PubMed ID."""
    client = CitedHealth()
    item = client.get_paper(pmid)

    if as_json:
        print(json.dumps(dataclasses.asdict(item)))  # noqa: T201
        return

    table = Table(title=f"Paper: PMID {item.pmid}")
    table.add_column("Property", style="cyan")
    table.add_column("Value")

    table.add_row("PMID", item.pmid)
    table.add_row("Title", item.title)
    table.add_row("Journal", item.journal)
    table.add_row("Year", str(item.publication_year or "[dim]—[/dim]"))
    table.add_row("Study Type", item.study_type or "[dim]—[/dim]")
    table.add_row("Citations", str(item.citation_count))
    table.add_row("Open Access", "Yes" if item.is_open_access else "No")
    table.add_row("PubMed Link", item.pubmed_link or "[dim]—[/dim]")

    console.print(table)


@app.command()
def conditions(
    as_json: Annotated[bool, typer.Option("--json", help="Output as compact JSON")] = False,
    featured: Annotated[bool | None, typer.Option("--featured/--all", help="Filter featured conditions only")] = None,
) -> None:
    """List health conditions."""
    client = CitedHealth()
    results = client.list_conditions(is_featured=featured)

    if as_json:
        print(json.dumps([dataclasses.asdict(r) for r in results]))  # noqa: T201
        return

    if not results:
        console.print("[yellow]No conditions found.[/yellow]")
        return

    table = Table(title="Conditions")
    table.add_column("Name", style="cyan")
    table.add_column("Slug")
    table.add_column("Prevalence")
    table.add_column("Featured", justify="center")

    for item in results:
        table.add_row(
            item.name,
            item.slug,
            item.prevalence or "[dim]—[/dim]",
            "Y" if item.is_featured else "",
        )

    console.print(table)
    console.print(f"[dim]{len(results)} result(s)[/dim]")


@app.command()
def condition(
    slug: Annotated[str, typer.Argument(help="Condition slug (e.g. 'hair-loss')")],
    as_json: Annotated[bool, typer.Option("--json", help="Output as compact JSON")] = False,
) -> None:
    """Get a single condition by slug."""
    client = CitedHealth()
    item = client.get_condition(slug)

    if as_json:
        print(json.dumps(dataclasses.asdict(item)))  # noqa: T201
        return

    table = Table(title=f"Condition: {item.name}")
    table.add_column("Property", style="cyan")
    table.add_column("Value")

    table.add_row("Name", item.name)
    table.add_row("Slug", item.slug)
    table.add_row("Description", item.description or "[dim]—[/dim]")
    table.add_row("Prevalence", item.prevalence or "[dim]—[/dim]")
    table.add_row("Symptoms", ", ".join(item.symptoms) if item.symptoms else "[dim]—[/dim]")
    table.add_row("Risk Factors", ", ".join(item.risk_factors) if item.risk_factors else "[dim]—[/dim]")
    table.add_row("Featured", "Yes" if item.is_featured else "No")

    console.print(table)


@app.command()
def glossary(
    category: Annotated[str | None, typer.Option("--category", "-c", help="Filter by category")] = None,
    as_json: Annotated[bool, typer.Option("--json", help="Output as compact JSON")] = False,
) -> None:
    """List glossary terms."""
    client = CitedHealth()
    results = client.list_glossary(category=category)

    if as_json:
        print(json.dumps([dataclasses.asdict(r) for r in results]))  # noqa: T201
        return

    if not results:
        console.print("[yellow]No glossary terms found.[/yellow]")
        return

    table = Table(title="Glossary")
    table.add_column("Term", style="cyan")
    table.add_column("Slug")
    table.add_column("Category")
    table.add_column("Abbreviation")

    for item in results:
        table.add_row(
            item.term,
            item.slug,
            item.category or "[dim]—[/dim]",
            item.abbreviation or "[dim]—[/dim]",
        )

    console.print(table)
    console.print(f"[dim]{len(results)} result(s)[/dim]")


@app.command()
def guides(
    category: Annotated[str | None, typer.Option("--category", "-c", help="Filter by category")] = None,
    as_json: Annotated[bool, typer.Option("--json", help="Output as compact JSON")] = False,
) -> None:
    """List health guides."""
    client = CitedHealth()
    results = client.list_guides(category=category)

    if as_json:
        print(json.dumps([dataclasses.asdict(r) for r in results]))  # noqa: T201
        return

    if not results:
        console.print("[yellow]No guides found.[/yellow]")
        return

    table = Table(title="Guides")
    table.add_column("Title", style="cyan", max_width=60)
    table.add_column("Slug")
    table.add_column("Category")

    for item in results:
        table.add_row(
            item.title[:60],
            item.slug,
            item.category or "[dim]—[/dim]",
        )

    console.print(table)
    console.print(f"[dim]{len(results)} result(s)[/dim]")


if __name__ == "__main__":
    app()
