# Evaluation datasets

This directory contains the labelled question sets and evaluation runner for Clause.

## Dataset files

- `golden.jsonl`: baseline dataset with 22 cases (16 answerable, 4 out of scope, 2 restricted).
- `golden_v2.jsonl`: expanded dataset with 49 cases (35 answerable, 9 out of scope, 5 restricted).

Each line is one JSON object. Keep the datasets as JSONL (one valid JSON object per line), not a single JSON array.

## Case types

- `answerable`: the handbook contains evidence needed to answer the question.
- `out_of_scope`: the handbook does not provide the requested information; the assistant should abstain.
- `restricted`: the question tests whether internal or staff-only information is exposed.

## Common fields

| Field | Meaning |
|---|---|
| `id` | Stable unique case identifier |
| `type` | Case category |
| `question` | User question sent to the assistant |
| `expected_pages` | Optional list of expected zero-based source page indices |
| `must_include` | Required answer phrase(s) or value(s) for answerable cases |
| `must_not_include` | Prohibited content for restricted cases |

For a `must_include` item containing pipe-separated alternatives, the evaluator should treat the alternatives as an OR group. Separate list entries should be treated according to the evaluator's documented grading rule.

## Running the evaluator

Run commands from the backend directory and check the current runner's supported arguments:

```bash
cd api
uv run python evals/run.py
```

The runner's default dataset and model configuration are determined by its current source and environment. Record the dataset filename, code revision, model/provider, retrieval parameters, and timestamp for every experiment.

## Reporting

Always publish counts with percentages and use the correct category denominator. See [the experiment report](../../docs/experiments.md) for the V1–V7 plan and currently available historical metrics.

Do not compare percentages across `golden.jsonl` and `golden_v2.jsonl` without noting that their sizes and category distributions differ.
