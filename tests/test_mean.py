import math
from pathlib import Path
from elixir_task.io import SSegmentFile, FFunctionFile
from elixir_task.analysis import covered_mean

def test_mean_small(tmp_path):
    s = tmp_path / 'a.s'
    f = tmp_path / 'b.f'
    s.write_text('2\t5\n', encoding='utf-8')  # covers indices 2,3,4
    f.write_text('\n'.join(['10','10','20','40','50'])+'\n', encoding='utf-8')
    m = covered_mean(SSegmentFile(s).iter_segments(), FFunctionFile(f).iter_values())
    assert abs(m - ((20+40+50)/3)) < 1e-12
