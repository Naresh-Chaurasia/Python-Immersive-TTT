# SupportPilot — Python Fundamentals Learning Series

Seven notebooks teaching the Python you need to read and extend the
**original SupportPilot project** (the plain-Python version — no
LangChain). Every concept is demonstrated against the real project code,
not disconnected toy examples.

## Setup

```bash
pip install -r requirements.txt   # only scikit-learn/numpy/pydantic needed; no LangChain
jupyter notebook                  # or jupyter lab
```

Run notebooks from *inside* this folder so `import database`, `import
retrieval`, `import llm_client`, etc. resolve correctly. **Every notebook
was actually executed end to end** while being built (not just
syntax-checked) — you should be able to run all cells top to bottom without
errors, using only the standard library plus `scikit-learn`. Pydantic is
only needed for notebook 3's optional structured-output demo cells, which
are clearly marked.

## Notebook order

| # | Notebook | Covers | Real project code you'll read |
|---|----------|--------|-------------------------------|
| 1 | `01_python_core_syntax.ipynb` | Functions, type hints, f-strings, control flow, default args | `escalation_rules.py` |
| 2 | `02_data_structures.ipynb` | dict/list/set/tuple, comprehensions, unpacking | `pipeline.py`, `agents.py` |
| 3 | `03_oop_classes_dataclasses_enums.ipynb` | Classes, `@dataclass`, `Enum`, Pydantic's `BaseModel` | `retrieval.py`, `models.py` |
| 4 | `04_modules_imports_project_structure.ipynb` | Modules, imports, `__main__` guard, dependency chains | the whole file layout |
| 5 | `05_regular_expressions.ipynb` | `re.search`, alternation, groups, `.*`, capture groups | `llm_client.py`'s mock classifier |
| 6 | `06_files_json_sqlite_cli.ipynb` | `pathlib`, `sqlite3`, `json`, `argparse`, `os.environ`, `datetime` | `database.py`, `main.py` |
| 7 | `07_reading_the_real_project.ipynb` | Everything combined — runs the real `pipeline.py` | all of the above |

Each notebook ends with a hands-on exercise that extends real project code.
Do these before moving on — notebook 7 in particular assumes you've
internalized, not just read, notebooks 1-6.

## A note on Python version

Notebook 3 includes a real gotcha you'll hit if you're not warned about it:
`str`-mixed `Enum` classes (`class IssueType(str, Enum)`) changed behavior
between Python versions — `str()`/f-strings on a member print
`"IssueType.FRAUD_SUSPECTED"` on Python 3.11+, not the raw value
`"fraud_suspected"`, even though equality (`==`) still works either way.
This was verified against the actual Python 3.12 behavior, not assumed —
worth remembering the next time an Enum "looks wrong" in a print statement.
