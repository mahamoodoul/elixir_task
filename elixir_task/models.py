from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Iterator, Tuple, Protocol, Optional

@dataclass(frozen=True)
class Segment:
    start: int
    end: int  # half-open [start, end)

    def length(self) -> int:
        return max(0, self.end - self.start)

class SegmentSource(Protocol):
    def iter_segments(self) -> Iterator[Segment]: ...

class FunctionSource(Protocol):
    def iter_values(self) -> Iterator[float]: ...
