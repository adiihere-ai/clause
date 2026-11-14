# Clause — AI-Powered Shop Assistant

Clause is a handbook-grounded customer-support assistant built with Retrieval-Augmented Generation (RAG). It answers shop-policy questions using information retrieved from a shop handbook and is designed to refuse questions that cannot be supported by the available handbook content.

The project explores how retrieval settings, prompts, model configuration, and hybrid retrieval affect answer quality and safe refusal behaviour.

> **Project status:** The repository documentation and evaluation plan are being assembled. Historical experiment results are labelled as historical; experiments without verified terminal output are not presented as completed.

## Project goals

- Answer customer questions using handbook evidence rather than unsupported model knowledge.
- Retrieve relevant handbook passages from a Qdrant vector store.
- Return source information with answers where available.
- Refuse out-of-scope questions when the handbook does not contain the answer.
- Prevent staff-only handbook material from entering the customer-facing retrieval index.
- Evaluate answer correctness, retrieval behaviour, refusal behaviour, and restricted-information leakage.

## Architecture at a glance

The backend is organized under `api/` and uses Python, FastAPI, LangChain, and Qdrant.

1. **Configuration** — `api/app/core/config.py` loads application and model settings.
2. **Ingestion** — `api/app/services/ingestion.py` loads the handbook, prepares document chunks, creates embeddings, and indexes them.
3. **Retrieval** — `api/app/services/retrieval.py` contains retrieval-related functionality.
4. **Answer generation** — `api/app/services/chat.py` combines the question and retrieved evidence and generates the response.
5. **API and CLI** — `api/app/main.py` exposes the API; `api/app/cli.py` provides a command-line entry point.
6. **Evaluation** — `api/evals/run.py` runs the golden question sets and reports evaluation outcomes.

The intended request flow is:

```text
Customer question
       |
       v
Question validation
       |
       v
Retrieve handbook passages from Qdrant
       |
       v
Relevance / evidence check
       |
       +---- insufficient evidence ----> Safe refusal
       |
       v
Generate an answer grounded in retrieved passages
       |
       v
Answer and source information
```

See [the architecture notes](docs/architecture.md) for more detail.

## Repository layout

```text
clause/
├── README.md
├── .gitignore
├── api/
│   ├── app/
│   │   ├── core/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── cli.py
│   │   └── main.py
│   ├── evals/
│   │   ├── golden.jsonl
│   │   ├── golden_v2.jsonl
│   │   └── run.py
│   ├── files/                 # Local source documents; publish only sanitized data
│   ├── .env.example
│   ├── pyproject.toml
│   └── uv.lock
├── docs/
│   ├── architecture.md
│   └── experiments.md
└── web/                       # Frontend directory; document its implementation as it is finalized
```

Generated vector databases, virtual environments, caches, and secrets should remain local and are excluded by `.gitignore`.

## Technology

The shared project configuration and architecture notes identify the following technologies:

- Python 3.13
- FastAPI
- LangChain
- Qdrant
- Dense embeddings and sparse retrieval components in the newer hybrid-retrieval implementation
- Ollama and/or a configured hosted chat-model provider
- `uv` for Python dependency and environment management

Exact model/provider settings are controlled by the environment configuration. Use `api/.env.example` as the template and check it against `api/app/core/config.py` before running the project.

## Setup

The commands below assume that the backend project is in `api/`.

1. Install Python 3.13 and [uv](https://docs.astral.sh/uv/).
2. Open a terminal in the `api/` directory.
3. Create your local environment file from the example:

   ```bash
   cp .env.example .env
   ```

   On Windows PowerShell:

   ```powershell
   Copy-Item .env.example .env
   ```

4. Add the credentials and model settings required by your selected provider to `.env`. Never commit this file.
5. Install the locked dependencies:

   ```bash
   uv sync --locked
   ```

6. Make sure the configured embedding and chat models are available. For Ollama-based models, install/start Ollama and pull the model names configured in your environment.
7. Follow the commands exposed by the current CLI and ingestion modules to build the local index before starting the API.

> The exact CLI subcommands and ingestion invocation must be confirmed against the current source files before being treated as definitive. This README intentionally does not invent command names.

## API

The project architecture describes a FastAPI service with a health route and a question-answering route:

- `GET /` — health/status endpoint.
- `POST /ask` — submits a customer question and returns an answer with source information.

Open the FastAPI Swagger UI at `/docs` after starting the backend to inspect the exact request and response schemas implemented by the current code.

## Evaluation

Two golden datasets are present in the project:

| Dataset | Cases | Answerable | Out of scope | Restricted |
|---|---:|---:|---:|---:|
| `golden.jsonl` | 22 | 16 | 4 | 2 |
| `golden_v2.jsonl` | 49 | 35 | 9 | 5 |

The datasets are different in size and composition. Their raw pass percentages should not be compared as if they were identical test sets.

The evaluation plan contains seven versions, V1–V7. The historical results and the intended change in each version are documented in [docs/experiments.md](docs/experiments.md). Results for any run must be supported by its actual terminal output or saved report.

## Security and data handling

The handbook contains material intended for staff as well as customer-facing policy information. **Staff-only content must be excluded before documents are chunked and embedded.** A prompt instruction alone is not an access-control boundary.

Before publishing or deploying:

- Do not commit `.env`, API keys, tokens, or other credentials.
- Do not commit local Qdrant/vector-store data.
- Do not publish an unredacted handbook containing staff-only material.
- Verify the ingested chunks/index contain no staff-only content.
- Keep restricted evaluation questions and expected leak terms safe to publish only after checking that they do not disclose confidential policy details.
- Rebuild and validate the index after changing the ingestion filter.

## Limitations

- RAG answers depend on the quality and coverage of the handbook and retrieval results.
- A correct passage being retrieved does not guarantee that the language model will produce a correct answer.
- Evaluation matching based on required keywords is an approximation, not a complete semantic correctness measure.
- Results from different golden datasets are not directly comparable without accounting for their different case composition.
- Model/provider settings, thresholds, and retrieval strategy must be recorded for each experiment.

## Experiments and results

See [docs/experiments.md](docs/experiments.md) for the V1–V7 plan, known historical results, metrics, and reproduction requirements.

## License

No license has been selected yet. Until a license is added, all rights are reserved by the copyright holder by default.
