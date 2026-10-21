# 0001: Archive on dataset_date end date

## Status

Accepted — 2026-10-20

## Context

Organisations were archived on `last_modified` being older than 6 months (3 months for ADAM).
`last_modified` reflects edits to the dataset rather than the period its data covers.
`dataset_date` is a range (`[start TO end]`) whose end may be `*` for ongoing datasets, so `parse_date`
cannot read it.

## Decision

- `before: dataset_date` compares the range end date, parsed with `DateHelper.get_time_period_info`
  (`hdx.api.utilities.date_helper`).
- All configured organisations use `dataset_date` with a 3-month cutoff.
- Ongoing datasets (`*` end) resolve to today, so are never archived. A missing `dataset_date` never matches.

## Consequences

Other `before` fields (e.g. `last_modified`) still work via `parse_date`.
Datasets with a recent `last_modified` but an old coverage end date will now be archived.
