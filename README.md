# ELIXIR 2025 Development Task — Python Solution

This repository implements the required analyses for **SEGMENT** (`.s`) and **FUNCTION** (`.f`) genomic files:

- **SEGMENT + SEGMENT** → total overlap **(number of positions)**
- **FUNCTION + FUNCTION** → **Pearson correlation** (sample)
- **SEGMENT + FUNCTION** → **mean** of FUNCTION values covered by SEGMENT regions

It is written in Python with a small, extensible architecture designed to support new file formats via a registry of parsers.

---

## Quickstart

### 1) Create a virtual environment (any OS) and install dependencies

#### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -r requirements.txt
```

#### Windows (PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt
```

> Only `pytest` is required for running tests. The solution itself uses only the Python standard library.

### 2) Run the CLI

```bash
python -m elixir_task <path_to_file_X> <path_to_file_Y> [--genome-length 10000000] [--output result.txt]
```

The program auto-detects file types by extension:
- `.s` → SEGMENT
- `.f` → FUNCTION
- **Extras (extensibility examples):**
  - `.bed` → BED3-like segments (chrom column ignored)
  - `.csv` → FUNCTION-like (one float per line)
  - `.const` → FUNCTION-like (single value replicated for the full genome, header like `value=3.14` or just `3.14`)

Examples:
```bash
python -m elixir_task tests/data/testfile_a.s tests/data/testfile_b.s
python -m elixir_task tests/data/testfile_a.f tests/data/testfile_b.f
python -m elixir_task tests/data/testfile_a.s tests/data/testfile_b.f
python -m elixir_task genome.bed signal.const --genome-length 1000000

```

> **Large fixtures skipped from Git** — The `tests/data/testfile_a.*` and
> `tests/data/testfile_b.*` files are huge synthetic datasets used for local
> stress-testing. They remain in `.gitignore`, so clone/pull operations stay
> lightweight. If you need them, drop equivalently named files into
> `tests/data/` (or generate your own) before running the commands above.

### 3) Run tests

```bash
pytest -q
```

---

## Design notes

- **Streaming algorithms** are used to handle very large files:
  - `.f` files (FUNCTION) are processed **line-by-line**.
  - `.s` files (SEGMENT) are assumed **sorted and non-overlapping**; two-pointer sweeps compute overlap and SEGMENT×FUNCTION means in **O(n)** without loading everything into memory.
- **Pearson correlation** is computed in one pass from five running sums:
  \(\sum x, \sum y, \sum x^2, \sum y^2, \sum xy\), avoiding large arrays.

### Extensibility

New formats can be added by registering a new parser in `elixir_task/registry.py`. See the examples for:
- `BedSegmentParser` (for `.bed`)
- `CSVFunctionParser` (for `.csv`)
- `ConstFunctionParser` (for `.const`)

---

## Repository layout

```
elixir-task/
├─ elixir_task/
│  ├─ __init__.py
│  ├─ cli.py                # entry point: python -m elixir_task
│  ├─ models.py             # core dataclasses and interfaces
│  ├─ analysis.py           # overlap, correlation, covered-mean
│  ├─ io.py                 # concrete parsers for .s and .f
│  ├─ registry.py           # registry and extra (extensible) formats
│  └─ utils.py              # small helpers (e.g. safe float parsing)
├─ tests/
│  ├─ test_overlap.py
│  ├─ test_correlation.py
│  ├─ test_mean.py
│  └─ data/ (small synthetic samples)
├─ requirements.txt
└─ README.md
```

---

## Notes & possible improvements

- For extremely large `.f` files on spinning disks, using buffered I/O and `readinto`/memoryview could further improve speed; current implementation is sufficient.
- If the genome length varies across projects, we already allow `--genome-length` to be provided.
- For real genomic BED files, supporting a chromosome column + genome mapping could be added in a future version.
