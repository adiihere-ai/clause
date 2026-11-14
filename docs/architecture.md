# Clause Architecture

## 1. System overview

Clause is a Retrieval-Augmented Generation (RAG) application for answering customer questions from a shop handbook. The backend is organized around configuration, ingestion, retrieval, response generation, and evaluation.

The central design principle is that the handbook is the source of truth. The language model should answer from retrieved handbook passages and abstain when those passages do not support an answer.

## 2. Main components

| Component | Location | Responsibility |
|---|---|---|
| Settings | `app/core/config.py` | Loads environment-based application and model settings |
| API | `app/main.py` | Exposes the backend HTTP interface |
| CLI | `app/cli.py` | Supports terminal-based interaction |
| Chat service | `app/services/chat.py` | Coordinates question answering and response generation |
| Ingestion service | `app/services/ingestion.py` | Loads, splits, embeds, and indexes handbook content |
| Retrieval service | `app/services/retrieval.py` | Handles retrieval functionality |
| Schemas | `app/schemas/` | Defines structured request and response data |
| Evaluation | `evals/run.py` | Runs labelled evaluation questions |

## 3. Ingestion flow

1. Read the authorized handbook PDF.
2. Extract page text while retaining page metadata.
3. Exclude internal/staff-only material before creating chunks.
4. Split the remaining content using the configured chunk size and overlap.
5. Create embeddings using the configured embedding model.
6. Store the vectors and associated text/metadata in Qdrant.
7. Validate the resulting collection and inspect indexed text for restricted material.

**Security requirement:** filtering must happen before embedding and indexing. Instructions in the generation prompt alone cannot guarantee that internal content is inaccessible.

A rebuild strategy should be safe: validate source extraction, filtering, and embedding dimensions before replacing a working collection. Where possible, build a new collection, validate it, and only then switch the application to it.

## 4. Question-answering flow

1. Receive a customer question through the API or CLI.
2. Validate and normalize the question.
3. Generate a query embedding.
4. Retrieve relevant chunks from Qdrant using the configured retrieval strategy.
5. Apply the relevance threshold or other retrieval gate.
6. If no evidence passes the gate, return the configured refusal response without asking the model to invent an answer.
7. Otherwise, provide the question and retrieved handbook passages to the chat model.
8. Return the answer together with available source metadata.

The current project history includes both dense retrieval and a later hybrid dense/sparse retrieval implementation. Exact runtime behaviour must be taken from the code and settings used for each experiment.

## 5. Data and model layer

- **Vector store:** Qdrant.
- **Dense embeddings:** configured through LangChain's embedding initialization.
- **Sparse retrieval:** the later hybrid implementation uses a sparse/BM25 component.
- **Chat model:** configured through LangChain's chat-model initialization.
- **Configuration:** environment variables use the `RAG_` prefix.

The project records include an example configuration using an Ollama embedding model with a 768-dimensional vector space and a Google GenAI chat provider. These are configuration examples, not a guarantee that every environment uses those providers.

## 6. Evaluation architecture

The evaluation harness reads JSONL cases, sends questions to the RAG service, and grades responses against expected evidence. The datasets distinguish:

- `answerable`: handbook-supported questions.
- `out_of_scope`: questions the handbook does not answer.
- `restricted`: questions designed to test whether internal information is exposed.

Evaluation should report category denominators, retrieval/page hit rate, evidence presence, answer correctness, refusal behaviour, and restricted-information leakage separately.

## 7. Operational considerations

- Embedded/local Qdrant storage can be locked to one process. Avoid running ingestion, API, CLI, and evaluation simultaneously against the same local storage directory.
- Use a Qdrant server when concurrent access is required.
- Record model, provider, temperature, top-k, score threshold, chunk settings, dataset version, and code revision with every evaluation.
- Keep local vector-store data and credentials out of version control.
- Never use prompt wording as the only protection for staff-only data.

## 8. Architecture evidence and caveats

The architecture description is based on the project source and architecture notes shared during development. Some historical notes describe earlier dense-only configurations, while the later implementation introduces hybrid retrieval. Treat each experiment as a snapshot of its own code and settings rather than assuming one configuration applied to all versions.
