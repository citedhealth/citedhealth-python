# citedhealth

[![PyPI](https://img.shields.io/pypi/v/citedhealth)](https://pypi.org/project/citedhealth/)
[![Python](https://img.shields.io/pypi/pyversions/citedhealth)](https://pypi.org/project/citedhealth/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Python client for the [CITED Health](https://citedhealth.com) evidence-based supplement API. Query 74 ingredients, 30 conditions, 152 evidence links, and 2,881 PubMed papers — every health claim backed by peer-reviewed research.

> **Try it live at [citedhealth.com](https://citedhealth.com)** — evidence grades for supplements like Biotin, Melatonin, and Ashwagandha.

<p align="center">
  <img src="demo.gif" alt="citedhealth CLI demo — search supplement ingredients, evidence grades, and PubMed papers" width="800">
</p>

## Table of Contents

- [Install](#install)
- [Quick Start](#quick-start)
- [Command-Line Interface](#command-line-interface)
- [What You Can Do](#what-you-can-do)
- [Evidence Grades](#evidence-grades)
- [API Reference](#api-reference)
- [Learn More About Evidence-Based Supplements](#learn-more-about-evidence-based-supplements)
- [Also Available](#also-available)
- [License](#license)

## Install

```bash
pip install citedhealth
```

## Quick Start

```python
from citedhealth import CitedHealth

client = CitedHealth()

# Search ingredients
ingredients = client.search_ingredients("biotin")
print(ingredients[0].name)  # "Biotin"

# Get evidence grade
evidence = client.get_evidence("biotin", "nutritional-deficiency-hair-loss")
print(f"Grade: {evidence.grade} — {evidence.grade_label}")
# Grade: A — Strong Evidence

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
```

## What You Can Do

### Search Supplement Ingredients

Find ingredients by name or keyword. Each ingredient includes category, mechanism of action, recommended dosage, and available forms.

### Look Up Evidence Grades

Every ingredient-condition pair has an A-F evidence grade calculated from peer-reviewed studies:

| Grade | Label | Criteria |
|-------|-------|----------|
| A | Strong Evidence | Multiple RCTs/meta-analyses, consistent positive results |
| B | Good Evidence | At least one RCT, mostly consistent |
| C | Some Evidence | Small studies, some positive signals |
| D | Very Early Research | In vitro, case reports, pilot studies |
| F | Evidence Against | <30% of studies show positive effects |

### Search PubMed Papers

Access 2,881 indexed papers with citation data from Semantic Scholar.

## API Reference

| Method | Description |
|--------|-------------|
| `search_ingredients(query)` | Search ingredients by name |
| `get_ingredient(slug)` | Get ingredient by slug |
| `get_evidence(ingredient, condition)` | Get evidence links |
| `get_evidence_by_id(pk)` | Get evidence link by ID |
| `search_papers(query)` | Search papers |
| `get_paper(pmid)` | Get paper by PubMed ID |

Full API documentation: [citedhealth.com/developers/](https://citedhealth.com/developers/)

## Learn More About Evidence-Based Supplements

- **Tools**: [Evidence Checker](https://citedhealth.com/api/evidence/) · [Ingredient Browser](https://citedhealth.com/) · [Paper Search](https://citedhealth.com/papers/)
- **Browse**: [Hair Health](https://haircited.com) · [Sleep Health](https://sleepcited.com) · [All Ingredients](https://citedhealth.com/api/ingredients/)
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
