from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional, Tuple, Union
from .io import SSegmentFile, FFunctionFile, BedSegmentParser, CSVFunctionParser, ConstFunctionParser
from .models import SegmentSource, FunctionSource

@dataclass
class ParserSpec:
    kind: str  # 'segment' or 'function'
    factory: Callable[..., object]

def guess_parser(path: Path, genome_length: Optional[int] = None) -> Tuple[str, object]:
    ext = path.suffix.lower()
    if ext == '.s':
        return ('segment', SSegmentFile(path))
    if ext == '.f':
        return ('function', FFunctionFile(path))
    if ext == '.bed':
        return ('segment', BedSegmentParser(path))
    if ext == '.csv':
        return ('function', CSVFunctionParser(path))
    if ext == '.const':
        if genome_length is None:
            raise ValueError("genome-length is required for .const function files")
        return ('function', ConstFunctionParser(path, genome_length))
    raise ValueError(f"Unsupported file extension: {ext}")
