# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Async API: every method has an `_async` twin using `httpx.AsyncClient`
  natively (sync client still uses `requests`).
- Pagination helpers `iter_*` / `iter_*_async` for leads, contacts, companies,
  tasks, catalog elements and tags — lazy, page management handled for you.
- GitHub Actions CI running tests + ruff + mypy on PRs and pushes.
- Contract tests for ~100 methods covering HTTP method, URL path and body
  for both sync and async variants.
- `uv` packaging via `pyproject.toml` / `uv.lock`, replacing `setup.py` and
  `requirements.txt`.
- New entity `LossReasons`: list, get, create, update, delete.
- New entity `Sources`: list, get, create, update, delete.
- New entity `Chats`: list, get, create, update.

### Changed

- HTTP client migrated to `httpx` for the async API.
- Strict mypy typing enabled (`disallow_untyped_defs`), types modernized to
  PEP 604 (`Optional`/`Union` -> `X | None`), stale `# type: ignore` removed.
- README split into `docs/` with per-entity references; async examples added;
  docs added for customers, notes, events, tags, loss_reasons, sources and chats.
- Package version bumped from `0.0.20` to `1.0.0`.

### Fixed

- Preserve zero timestamps in filters (e.g. `updated_at__from=0`).
- `link_unsorted` URL was missing a slash between `crm_url` and `api/v4/...`.
- `_mask` and `__str__` typing.

### Security

- OAuth client auto-refreshes the access token on a `401` response and
  retries the request once (existing behaviour, covered by tests).

### Retry

- Retry with exponential backoff now also applies to `5xx` responses in
  addition to `429` and connection errors.

## [0.0.20] - 2026

- fix: use `closed_to` for the closed_at upper bound.
- fix: handle connection errors with retries (`_connection_counter`).

## [0.0.18] - 2025

- add `filter_ids` for `get_leads` and `_get_entities` method.

## [0.0.16] - 2025

- update get custom fields methods.

## [0.0.15] - 2025

- fix: subscribe webhook method.

## [0.0.14] - 2025

- add entity notes methods, rename
  `updatecustomers_segments_custom_fields` -> `update_customers_segments_custom_fields`.
- fix: create & update notes; slashes in notes, custom_fields, tags endpoints.

## [0.0.13] - 2025

- handle 429 error.
- fix: closed_at filter.

## [0.0.12] - 2025

- add mypy, fix get_events filters.

## [0.0.11] - 2025

- events method added.

## [0.0.10] - 2025

- fix url for unsorted leads.

## [0.0.9] - 2025

- fix filters: add `__from`, `__to` to timestamp fields filter query.
- fix contacts params.

## [0.0.4] - 2024

- fix link methods: amo api now returns status 200 with empty body.
- fix Amo api exceptions.
