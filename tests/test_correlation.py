import math
from pathlib import Path
from elixir_task.io import FFunctionFile
from elixir_task.analysis import pearson_correlation

def test_corr_known(tmp_path):
    p1 = tmp_path / 'a.f'
    p2 = tmp_path / 'b.f'
    p1.write_text('\n'.join(['1','2','3','4','5'])+'\n', encoding='utf-8')
    p2.write_text('\n'.join(['2','4','6','8','10'])+'\n', encoding='utf-8')
    r = pearson_correlation(FFunctionFile(p1).iter_values(), FFunctionFile(p2).iter_values())
    assert abs(r - 1.0) < 1e-12
