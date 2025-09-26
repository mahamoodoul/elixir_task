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
cd elixir_task 
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
python -m elixir_task tests/data/genome.bed tests/data/sample_function.const --genome-length 1000000

```

> **Large fixtures skipped from Git** — The `tests/data/testfile_a.*` and
> `tests/data/testfile_b.*` files are huge synthetic datasets used for local
> testing. They remain in `.gitignore`, so clone/pull operations stay
> lightweight. Adjust testfiles simply keeping tests/data directory
> (defaults to a genome length of 10,000,000) before running the commands above.




### 4) Run tests

```bash
pytest -q 

python -m pytest -vv
```

---

## Algorithmic Performance

- **`overlap_length`** — two-pointer sweep over the sorted segment lists. Each iteration advances one iterator, so every segment from both inputs is touched once. Time `O(n + m)`, space `O(1)`. This matches the Ω(n+m) lower bound because every segment must be examined.


- **`covered_mean`** — adapts to coverage. For light coverage it sums values directly over the covered indices (`O(L)`, where L is total covered length). For heavy coverage it builds a prefix array once (`O(n)`) and answers each segment in `O(1)` (`O(n + k)` overall, k = segments). It chooses the faster path, so runtime is `O(min(L, n + k))`; extra space only when prefix sums are needed.


- **`pearson_correlation`** — single pass with running sums for means, sums of squares, and cross-products. Needs one traversal of both series, giving time `O(n)` and space `O(1)`, which is optimal because every pair has to be read at least once.

These streaming-style approaches keep memory usage low, allow iterables/generators as inputs, and meet the theoretical lower bounds for the respective problems.

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
│  └─ data/ (samples test data (large test data can be added here for testing))
├─ requirements.txt
└─ README.md
```

---

## Notes & possible improvements

- For extremely large `.f` files on spinning disks, using buffered I/O and `readinto`/memoryview could further improve speed; current implementation is sufficient.
- If the genome length varies across projects, we already allow `--genome-length` to be provided.
- For real genomic BED files, supporting a chromosome column + genome mapping could be added in a future if needed.
