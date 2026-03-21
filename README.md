# citedhealth

[![PyPI version](https://agentgif.com/badge/pypi/citedhealth/version.svg)](https://pypi.org/project/citedhealth/)
[![Python](https://img.shields.io/pypi/pyversions/citedhealth)](https://pypi.org/project/citedhealth/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://agentgif.com/badge/github/citedhealth/citedhealth-python/stars.svg)](https://github.com/citedhealth/citedhealth-python)

Python client for the [CITED Health](https://citedhealth.com) evidence-based supplement API. Query 188 ingredients, 84 conditions, 323 evidence links, and 6,197 peer-reviewed papers across 6 health domains — every health claim backed by peer-reviewed research.

CITED Health covers 6 specialized health sites: [HairCited](https://haircited.com) (hair & scalp health), [SleepCited](https://sleepcited.com) (sleep quality), [GutCited](https://gutcited.com) (digestive health), [ImmuneCited](https://immunecited.com) (immune support), [BrainCited](https://braincited.com) (cognitive health), and the [CITED Health hub](https://citedhealth.com) — all powered by a unified evidence grading engine.

> **Try it live at [citedhealth.com](https://citedhealth.com)** — evidence grades for supplements like Biotin, Melatonin, and Ashwagandha.

<p align="center">
  <a href="https://agentgif.com/T9MeMry2"><img src="https://media.agentgif.com/T9MeMry2.gif" alt="citedhealth Python CLI demo — search supplement ingredients, evidence grades, and PubMed papers" width="800"></a>
</p>

## Table of Contents

- [Install](#install)
- [Quick Start](#quick-start)
- [Command-Line Interface](#command-line-interface)
- [What You Can Do](#what-you-can-do)
  - [Search Supplement Ingredients](#search-supplement-ingredients)
  - [Look Up Evidence Grades](#look-up-evidence-grades)
  - [Browse Health Conditions](#browse-health-conditions)
  - [Explore Glossary Terms](#explore-glossary-terms)
  - [Read Health Guides](#read-health-guides)
  - [Search PubMed Papers](#search-pubmed-papers)
- [Async Client](#async-client)
- [Evidence Grades](#evidence-grades)
- [API Reference](#api-reference)
- [Learn More About Evidence-Based Supplements](#learn-more-about-evidence-based-supplements)
- [Also Available](#also-available)
- [License](#license)

## Install

```bash
pip install citedhealth
```

With CLI support:

```bash
pip install citedhealth[cli]
```

## Quick Start

```python
from citedhealth import CitedHealth

client = CitedHealth()

# Search ingredients by name
ingredients = client.search_ingredients("biotin")
print(ingredients[0].name)  # "Biotin"

# Get evidence grade for an ingredient-condition pair
evidence = client.get_evidence("biotin", "nutritional-deficiency-hair-loss")
print(f"Grade: {evidence.grade} — {evidence.grade_label}")
# Grade: A — Strong Evidence

# Browse health conditions
conditions = client.list_conditions(is_featured=True)
for c in conditions:
    print(f"{c.name}: {c.prevalence}")

# Look up glossary terms
terms = client.list_glossary(category="vitamins")
for t in terms:
    print(f"{t.term}: {t.short_definition}")

# Search PubMed papers
papers = client.search_papers("biotin hair loss")
print(f"{len(papers)} papers found")
```

## Command-Line Interface

Install with the `cli` extra for terminal access:

```bash
pip install citedhealth[cli]
```

### Search ingredients

```bash
citedhealth ingredients biotin
```

### Get evidence grade for an ingredient-condition pair

```bash
citedhealth evidence biotin nutritional-deficiency-hair-loss
```

### Look up a single ingredient

```bash
citedhealth ingredient biotin
```

### List health conditions

```bash
citedhealth conditions
citedhealth conditions --featured
citedhealth condition hair-loss
```

### Browse glossary terms

```bash
citedhealth glossary
citedhealth glossary --category vitamins
```

### List health guides

```bash
citedhealth guides
citedhealth guides --category hair
```

### Search PubMed papers

```bash
citedhealth papers --year 2024
```

### Get a paper by PubMed ID

```bash
citedhealth paper 12345678
```

All commands support `--json` for machine-readable output:

```bash
citedhealth ingredients biotin --json
citedhealth conditions --json
```

## What You Can Do

### Search Supplement Ingredients

Find ingredients by name or keyword across 188 supplements. Each ingredient includes category, mechanism of action, recommended dosage, and available forms.

```python
client = CitedHealth()

# Search by keyword
results = client.search_ingredients("magnesium")
for ing in results:
    print(f"{ing.name} ({ing.category}) — {', '.join(ing.forms)}")

# Get full details for a single ingredient
biotin = client.get_ingredient("biotin")
print(f"Mechanism: {biotin.mechanism}")
print(f"Dosage: {biotin.recommended_dosage}")
```

### Look Up Evidence Grades

Every ingredient-condition pair has an A-F evidence grade calculated from peer-reviewed studies. The 323 evidence links span all 6 health domains.

```python
# Check evidence for a specific supplement claim
evidence = client.get_evidence("melatonin", "insomnia")
print(f"Grade {evidence.grade}: {evidence.grade_label}")
print(f"Based on {evidence.total_studies} studies, {evidence.total_participants} participants")
print(f"Direction: {evidence.direction}")
```

### Browse Health Conditions

Access 84 health conditions across 6 domains — hair loss, insomnia, IBS, immune deficiency, brain fog, and more. Each condition includes prevalence data, symptoms, and risk factors.

```python
# List all featured conditions
conditions = client.list_conditions(is_featured=True)
for c in conditions:
    print(f"{c.name} — {c.prevalence}")
    print(f"  Symptoms: {', '.join(c.symptoms[:3])}")

# Get condition details
condition = client.get_condition("hair-loss")
print(f"Risk factors: {', '.join(condition.risk_factors)}")
```

### Explore Glossary Terms

Browse 228 glossary terms covering supplement science, pharmacology, and nutrition terminology.

```python
# List glossary terms by category
terms = client.list_glossary(category="vitamins")
for t in terms:
    print(f"{t.term} ({t.abbreviation}): {t.short_definition}")

# Get a specific term
term = client.get_glossary_term("bioavailability")
print(f"{term.term}: {term.definition}")
```

### Read Health Guides

Access 50 health guides with evidence-based recommendations for supplement use.

```python
# List all guides
guides = client.list_guides()
for g in guides:
    print(f"{g.title} [{g.category}]")

# Get full guide content
guide = client.get_guide("biotin-for-hair-growth")
print(guide.content)
```

### Search PubMed Papers

Access 6,197 PubMed-indexed papers with citation data from Semantic Scholar.

```python
# Search by keyword
papers = client.search_papers("vitamin D immune")
for p in papers:
    print(f"[{p.pmid}] {p.title} ({p.publication_year})")

# Filter by year
recent = client.search_papers(year=2024)
print(f"{len(recent)} papers published in 2024")
```

## Async Client

For async applications, use `AsyncCitedHealth`:

```python
import asyncio
from citedhealth import AsyncCitedHealth

async def main():
    async with AsyncCitedHealth() as client:
        # All methods available as async versions
        ingredients = await client.search_ingredients("zinc")
        conditions = await client.list_conditions(is_featured=True)
        glossary = await client.list_glossary()
        guides = await client.list_guides()
        evidence = await client.get_evidence("zinc", "immune-function")
        print(f"Grade: {evidence.grade}")

asyncio.run(main())
```

## Evidence Grades

| Grade | Label | Criteria |
|-------|-------|----------|
| A | Strong Evidence | Multiple RCTs/meta-analyses, consistent positive results |
| B | Good Evidence | At least one RCT, mostly consistent |
| C | Some Evidence | Small studies, some positive signals |
| D | Very Early Research | In vitro, case reports, pilot studies |
| F | Evidence Against | <30% of studies show positive effects |

## API Reference

| Method | Description |
|--------|-------------|
| `search_ingredients(query, category)` | Search ingredients by name or category |
| `get_ingredient(slug)` | Get ingredient by slug |
| `get_evidence(ingredient, condition)` | Get evidence for an ingredient-condition pair |
| `get_evidence_by_id(pk)` | Get evidence link by ID |
| `search_papers(query, year)` | Search PubMed papers |
| `get_paper(pmid)` | Get paper by PubMed ID |
| `list_conditions(is_featured)` | List health conditions |
| `get_condition(slug)` | Get condition by slug |
| `list_glossary(category)` | List glossary terms |
| `get_glossary_term(slug)` | Get glossary term by slug |
| `list_guides(category)` | List health guides |
| `get_guide(slug)` | Get guide by slug |

Full API documentation: [citedhealth.com/developers/](https://citedhealth.com/developers/)

OpenAPI spec: [citedhealth.com/api/openapi.json](https://citedhealth.com/api/openapi.json)

## Learn More About Evidence-Based Supplements

- **Sites**: [Hair Health](https://haircited.com) · [Sleep Health](https://sleepcited.com) · [Gut Health](https://gutcited.com) · [Immune Health](https://immunecited.com) · [Brain Health](https://braincited.com) · [Hub](https://citedhealth.com)
- **Tools**: [Evidence Checker](https://citedhealth.com/api/evidence/) · [Ingredient Browser](https://citedhealth.com/) · [Paper Search](https://citedhealth.com/papers/)
- **Guides**: [Grading Methodology](https://citedhealth.com/editorial-policy/) · [Medical Disclaimer](https://citedhealth.com/medical-disclaimer/)
- **API**: [REST API Docs](https://citedhealth.com/developers/) · [OpenAPI Spec](https://citedhealth.com/api/openapi.json)

## Also Available

| Platform | Install | Link |
|----------|---------|------|
| **npm** | `npm install citedhealth` | [npm](https://www.npmjs.com/package/citedhealth) |
| **Go** | `go get github.com/citedhealth/citedhealth-go` | [pkg.go.dev](https://pkg.go.dev/github.com/citedhealth/citedhealth-go) |
| **Rust** | `cargo add citedhealth` | [crates.io](https://crates.io/crates/citedhealth) |
| **Ruby** | `gem install citedhealth` | [RubyGems](https://rubygems.org/gems/citedhealth) |
| **MCP** | `uvx citedhealth-mcp` | [PyPI](https://pypi.org/project/citedhealth-mcp/) |

## License

MIT — see [LICENSE](LICENSE).
