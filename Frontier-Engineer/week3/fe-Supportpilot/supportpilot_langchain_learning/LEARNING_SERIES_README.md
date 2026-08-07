# SupportPilot — LangChain Learning Series

Six notebooks that teach LangChain from scratch, using the SupportPilot
project's real code as the running example instead of toy snippets.

## Setup

```bash
pip install -r requirements.txt
jupyter notebook   # or jupyter lab
```

Open the notebooks in order — each builds on concepts from the last, and
several later notebooks `import` code straight from the earlier ones'
explanations. Run them from *inside* this folder (`supportpilot_langchain/`)
so `import database`, `import models`, `import tools`, etc. resolve.

**No API key is required for any notebook.** Everything is demonstrated with
LangChain's built-in `FakeListChatModel` and the project's offline TF-IDF
embeddings. Each notebook has a clearly marked (commented) section showing
what changes with a real `ANTHROPIC_API_KEY`.

## Notebook order

| # | Notebook | Covers |
|---|----------|--------|
| 1 | `01_langchain_foundations.ipynb` | Messages, chat models, `ChatPromptTemplate`, your first `\|` chain |
| 2 | `02_output_parsers_structured_output.ipynb` | `StrOutputParser`, `PydanticOutputParser`, `with_structured_output` |
| 3 | `03_lcel_and_runnables.ipynb` | `RunnableLambda`, `RunnableSequence`, `RunnableParallel` |
| 4 | `04_tools_and_function_calling.ipynb` | `@tool`, direct invocation vs. model-driven tool selection |
| 5 | `05_embeddings_vectorstores_retrieval.ipynb` | `Embeddings` interface, FAISS, retrievers (RAG) |
| 6 | `06_full_pipeline_walkthrough.ipynb` | Everything combined — runs the real `pipeline.py` end to end |

Every notebook ends with a hands-on exercise that extends the real project
code (not a disconnected toy problem) — do these before moving to the next
notebook; later notebooks assume you've seen the earlier project modules
run, not just read about them.

## A note on how these were built

These notebooks were authored and syntax-checked (every code cell parses as
valid Python via `ast.parse`), but LangChain itself wasn't installed in the
environment used to write them, so the LangChain-dependent cells were not
executed end-to-end before delivery. Run notebook 1 first and confirm the
early `FakeListChatModel` cells work in your environment before working
through the rest — if an import path has moved in the LangChain version you
installed, it should only require a small fix (check LangChain's own
migration notes), not a rewrite.
