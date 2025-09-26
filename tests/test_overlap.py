import math
from pathlib import Path
from elixir_task.io import SSegmentFile
from elixir_task.analysis import overlap_length

def test_overlap_simple(tmp_path):
    p1 = tmp_path / 'a.s'
    p2 = tmp_path / 'b.s'
    p1.write_text('0\t10\n20\t30\n', encoding='utf-8')
    p2.write_text('5\t25\n', encoding='utf-8')
    a = SSegmentFile(p1).iter_segments()
    b = SSegmentFile(p2).iter_segments()
    # overlaps: [5,10)=5 and [20,25)=5 -> total 10
    assert overlap_length(a, b) == 10
