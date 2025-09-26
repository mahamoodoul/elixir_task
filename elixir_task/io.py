from __future__ import annotations
from typing import Iterator, Iterable, List, Optional
from pathlib import Path
from .models import Segment, SegmentSource, FunctionSource
from .utils import to_int, to_float, safe_strip

class SSegmentFile(SegmentSource):
    """Parser for `.s` files: two integers per line: start<TAB>end, half-open [start,end).
    Assumes lines are sorted and non-overlapping (verification not enforced for optimization).
    """
    def __init__(self, path: Path):
        self.path = Path(path)
    def iter_segments(self) -> Iterator[Segment]:
        with self.path.open('r', encoding='utf-8') as fh:
            for line in fh:
                line = safe_strip(line)
                if not line or line.startswith('#'):
                    continue
                parts = line.split()
                if len(parts) < 2:
                    continue
                start = to_int(parts[0]); end = to_int(parts[1])
                yield Segment(start, end)

class FFunctionFile(FunctionSource):
    """Parser for `.f` files: one float per line."""
    def __init__(self, path: Path):
        self.path = Path(path)
    def iter_values(self) -> Iterator[float]:
        with self.path.open('r', encoding='utf-8') as fh:
            for line in fh:
                line = safe_strip(line)
                if line == '' or line.startswith('#'):
                    continue
                yield to_float(line)




# Extra formats for extensibility
class BedSegmentParser(SSegmentFile):
    """Simple BED-like parser: [chrom]\tstart\tend (0-based, half-open).
    Ignores the chromosome column.
    """
    def iter_segments(self) -> Iterator[Segment]:
        with self.path.open('r', encoding='utf-8') as fh:
            for line in fh:
                line = safe_strip(line)
                if not line or line.startswith('#'):
                    continue
                parts = line.split()
                if len(parts) < 3:
                    continue
                start = to_int(parts[1]); end = to_int(parts[2])
                yield Segment(start, end)

class CSVFunctionParser(FFunctionFile):
    """CSV parser for function values. Accepts comma or semicolon separated lists,
    or one value per line. Non-numeric fields are ignored.
    """
    def iter_values(self) -> Iterator[float]:
        with self.path.open('r', encoding='utf-8') as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                # split on comma/semicolon/whitespace
                for tok in line.replace(';', ',').replace('\t', ',').split(','):
                    tok = tok.strip()
                    if tok:
                        try:
                            yield float(tok)
                        except ValueError:
                            continue

class ConstFunctionParser(FunctionSource):
    """A constant function over a given genome length.
    The file contains a single value like '3.14' or 'value=3.14'.
    """
    def __init__(self, path: Path, genome_length: int):
        self.path = Path(path)
        self.genome_length = genome_length
    def iter_values(self) -> Iterator[float]:
        txt = self.path.read_text(encoding='utf-8').strip()
        if '=' in txt:
            txt = txt.split('=', 1)[1].strip()
        val = float(txt)
        for _ in range(self.genome_length):
            yield val
