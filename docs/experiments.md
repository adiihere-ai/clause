# V1–V7 Experiment Plan and Results

## 1. Purpose

The experiment series studies how changes to prompting, model settings, retrieval depth, ingestion filtering, model choice, and hybrid retrieval affect Clause.

A result is meaningful only when it is tied to its code version, dataset, model/provider, and run configuration. Historical outputs are kept separate from planned or newly reproduced runs.

## 2. Dataset versions

| Dataset | Total | Answerable | Out of scope | Restricted |
|---|---:|---:|---:|---:|
| `golden.jsonl` | 22 | 16 | 4 | 2 |
| `golden_v2.jsonl` | 49 | 35 | 9 | 5 |

The datasets have different sizes and category distributions. Raw percentages from one dataset should not be compared directly with percentages from the other without explaining the different denominators and case composition.

## 3. Final experiment plan

| Version | Experiment | Dataset in the plan | Main question |
|---|---|---|---|
| V1 | Original baseline | `golden.jsonl` | How does the original RAG pipeline perform? |
| V2 | Simple system prompt and prompt template | `golden.jsonl` | Does a clearer prompt improve grounded answers and refusals? |
| V3 | Temperature set to 0 | `golden.jsonl` | Does deterministic generation change answer consistency? |
| V4 | Model comparison | `golden.jsonl` | How does changing the chat model affect quality and refusal behaviour? |
| V5 | Top-k set to 2 | `golden.jsonl` | Does retrieving fewer chunks improve relevance or answer quality? |
| V6 | Remove staff-only section during ingestion | `golden.jsonl` | Does excluding internal content at indexing time prevent exposure? |
| V7 | Final hybrid RAG implementation | `golden_v2.jsonl` | How does the final hybrid implementation perform on the expanded test set? |

For V3–V6, preserve the planned single-variable change as far as possible. Record any additional changes rather than silently combining them.

## 4. Metrics and denominators

Report counts as well as percentages.

- **Retrieval/page hit rate:** answerable cases for which a source from an expected page is retrieved, divided by answerable cases.
- **Fact present in chunks:** answerable cases for which the required evidence is found in the retrieved context, divided by answerable cases. State whether the same score threshold and retrieval path as the live application were used.
- **Answer correctness:** answerable cases satisfying the expected answer criteria, divided by answerable cases.
- **Out-of-scope refusal rate:** out-of-scope cases correctly refused, divided by out-of-scope cases.
- **Restricted-information leak rate:** restricted cases whose responses contain prohibited information, divided by restricted cases.

If a category has no cases, report `n/a`, not zero.

A simple substring check is not sufficient for numeric facts: for example, searching for `5` can accidentally match `50,000`. Use token-aware numeric matching and clearly defined phrase alternatives.

## 5. Historical results currently available

The following are historical records shared during project development. They are not claims that the current repository code has just been executed.

### V1 — Original baseline

Dataset: `golden.jsonl` (22 cases; 16 answerable, 4 out of scope, 2 restricted).

| Metric | Historical result |
|---|---:|
| Retrieval/page hit rate | 100% |
| Fact present in chunks | 100% |
| Answer correctness | 44% |
| Out-of-scope refusal rate | 75% |
| Restricted-information leak rate | 100% |

The historical output showed that several answers were incorrect even when the expected fact was present in the retrieved chunks. Both restricted test questions exposed internal-only information in that run.

### V2 — Simple prompt and prompt template

Dataset: `golden.jsonl` (22 cases).

| Metric | Historical result |
|---|---:|
| Retrieval/page hit rate | 100% |
| Fact present in chunks | 100% |
| Answer correctness | 25% |
| Out-of-scope refusal rate | 100% |
| Restricted-information leak rate | 0% |

The historical result indicates a trade-off: the stricter prompt stopped the observed restricted-information leaks and improved out-of-scope refusals, but answer correctness fell compared with V1.

### Earlier V7 architecture snapshot

A previously shared architecture report records a run of **9/22 passed** on the 22-case dataset. It reports retrieval hit rate 100%, fact present in chunks 100%, answer correctness 18.8% (3/16), out-of-scope refusal 100% (4/4), and restricted-information leak rate 0% (0/2).

That report describes an earlier V7 snapshot and explicitly notes implementation caveats, including temperature not being passed to the chat model and an evaluation diagnostic retrieving chunks without the live threshold. Do not treat this 22-case report as the final 49-case V7 result.

## 6. V3–V6 status

The experiment plan defines V3–V6, but complete verified terminal outputs and matching configurations have not yet been consolidated here. Until those records are reproduced or supplied, their results must be labelled **not yet verified** rather than estimated or inferred.

## 7. V7 final run

The final plan assigns V7 to the hybrid RAG implementation and `golden_v2.jsonl` (49 cases). The final V7 report should include:

- Exact commit or source revision.
- Dataset filename and case counts by category.
- Chat provider and model.
- Embedding provider, model, and dimension.
- Dense/sparse retrieval settings.
- Top-k and relevance threshold.
- Chunk size and overlap.
- All case-level outcomes.
- Aggregate metrics with numerator and denominator.
- Full terminal output and a machine-readable report.

Do not substitute the earlier 9/22 architecture snapshot for this 49-case final evaluation.

## 8. Reproducibility checklist

For every run:

1. Confirm the dataset path and validate every JSONL record.
2. Record a version label and the exact configuration.
3. Ensure the Qdrant collection was built from the intended sanitized handbook.
4. Confirm staff-only material is absent from indexed chunks.
5. Run the evaluation without other processes accessing the same embedded Qdrant directory.
6. Save the complete terminal output.
7. Save case-level outcomes and aggregate metrics.
8. Record the timestamp, model/provider, and code revision.
9. Inspect failed cases manually before drawing conclusions.

## 9. Security experiment: staff-only material

The handbook contains customer-facing policy content and an internal staff-only section. The security objective is to ensure internal material is excluded **before chunking and embedding**. Prompt instructions are not an adequate substitute for ingestion-time filtering.

A successful restricted-question test is useful but does not prove the vector database contains no internal text. Validate the extracted source and indexed chunks directly. Do not publish the original handbook or local vector-store files if they contain confidential content.
