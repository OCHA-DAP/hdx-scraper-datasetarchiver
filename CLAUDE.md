# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This pipeline archives stale HDX datasets. It reads a per-organisation configuration
(`config/project_configuration.yaml`) that specifies match criteria — e.g. a `data_update_frequency`
value and a `before` clause (fields that must be older than a given relative date) — and, for each
configured organisation, searches HDX for datasets belonging to it and marks any matching, not-yet-archived
dataset as `archived` via the CKAN API. Currently configured for the `advanced-disaster-analysis-mapping`
(WFP ADAM), `unosat`, and `philsa` organisations, archiving datasets whose `data_update_frequency` is `-1`
and whose `last_modified` is more than 6 months old.

## Architecture

- `src/hdx/scraper/datasetarchiver/__main__.py` — entry point; reads HDX `Configuration` and calls `archive`
  with the current UTC time.
- `src/hdx/scraper/datasetarchiver/archive_datasets.py` — `archive()`: for each organisation in the
  config, resolves relative `before` dates against `today`, searches HDX for that organisation's datasets,
  and archives (via `Dataset.update_in_hdx`) those matching the configured criteria that aren't already
  archived. Returns the archived, not-archived, and already-archived dataset lists.
- `config/project_configuration.yaml` — per-organisation archiving criteria.

## Commands

Environment setup (Python 3.13, managed with `uv`):

```shell
uv sync
```

Run the pipeline (requires `~/.hdx_configuration.yaml` with an HDX key, and `~/.useragents.yaml`
with a `hdx-scraper-datasetarchiver` entry — see README.md):

```shell
uv run python -m hdx.scraper.datasetarchiver
```

Run all tests (with coverage, configured in `pyproject.toml`):

```shell
uv run pytest
```

Lint and format:

```shell
uv run ruff check
uv run ruff format
```

Pre-commit (runs ruff on every commit once installed):

```shell
pre-commit install
pre-commit run --all-files
```

Build:

```shell
uv build
```

Adding a dependency: add it to `project.dependencies` in `pyproject.toml` (or `[dependency-groups]`
for test-only deps), then run `uv lock --upgrade` to refresh `uv.lock` (pre-commit also does this
automatically on commit).

## Code Style

- Formatted with `ruff` via pre-commit hooks. After changing any Python code, run:

```bash
pre-commit run --all-files
```

- Python ≥ 3.13

## Collaboration Style

- Be objective, not agreeable. Act as a partner, not a sycophant. Push back when you disagree, flag
  tradeoffs honestly, and don't sugarcoat problems.
- Keep explanations brief and to the point.
- Don't rely on recalled knowledge for facts that could be stale (API behaviour, library versions,
  external systems). Search or read the actual source first. If you lack verified information, say
  so rather than speculate.

## Scope of Changes

When fixing a bug or addressing PR feedback, change only what is necessary to resolve the specific
issue. Do not refactor surrounding code, rename variables, adjust formatting, or make improvements
in the same commit unless they are directly required by the fix. Unrelated changes obscure the
intent of the fix and complicate review and blame.

## Decision Records

Non-trivial design decisions are recorded in `docs/decisions/` (see `docs/decisions/README.md`) —
the distilled decision, not the full planning narrative, belongs here.
