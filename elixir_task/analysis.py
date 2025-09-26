from __future__ import annotations
from typing import Iterator, Iterable, Tuple
from .models import Segment, SegmentSource, FunctionSource

def overlap_length(a: Iterable[Segment], b: Iterable[Segment]) -> int:
    """Compute total overlap length between two *sorted, non-overlapping* segment lists.
    Segments are half-open [start, end).
    """
    it_a = iter(a)
    it_b = iter(b)
    try:
        sa = next(it_a)
    except StopIteration:
        return 0
    try:
        sb = next(it_b)
    except StopIteration:
        return 0
    total = 0
    while True:
        # overlap between sa and sb
        lo = max(sa.start, sb.start)
        hi = min(sa.end, sb.end)
        if hi > lo:
            total += hi - lo
        # advance the one that ends first
        if sa.end <= sb.end:
            try:
                sa = next(it_a)
            except StopIteration:
                break
        else:
            try:
                sb = next(it_b)
            except StopIteration:
                break
    return total

def covered_mean(segments: Iterable[Segment], values: Iterable[float]) -> float:
    """Mean of function values for indices covered by *any* segment.
    Assumes segments are sorted, non-overlapping, values are indexed from 0 increasing by 1.
    """
    seg_it = iter(segments)
    try:
        cur = next(seg_it)
    except StopIteration:
        return float('nan')
    ssum = 0.0
    count = 0
    for idx, v in enumerate(values):
        # advance segment pointer until segment may cover idx
        while cur.end <= idx:
            try:
                cur = next(seg_it)
            except StopIteration:
                # we've passed all segments
                return (ssum / count) if count>0 else float('nan')
        if cur.start <= idx < cur.end:
            ssum += v
            count += 1
        elif idx < cur.start:
            continue
    return (ssum / count) if count>0 else float('nan')

def pearson_correlation(x: Iterable[float], y: Iterable[float]) -> float:
    """Sample Pearson correlation r for paired series x,y of equal length.
    One pass using running sums.
    """
    n = 0
    sx = sy = sxx = syy = sxy = 0.0
    itx = iter(x)
    ity = iter(y)
    for a, b in zip(itx, ity):
        n += 1
        sx += a
        sy += b
        sxx += a*a
        syy += b*b
        sxy += a*b
    if n < 2:
        return float('nan')
    # sample covariance denominator (n-1)
    num = sxy - (sx*sy)/n
    denom_x = sxx - (sx*sx)/n
    denom_y = syy - (sy*sy)/n
    denom = (denom_x * denom_y) ** 0.5
    if denom == 0.0:
        return float('nan')
    return num / denom
