from pathlib import Path
import math
import pytest

from elixir_task.analysis import pearson_correlation
from elixir_task.registry import guess_parser

DATA_DIR = Path(__file__).parent / "data"


def _values(path: Path, genome_length: int | None = None):
    kind, parser = guess_parser(path, genome_length=genome_length)
    assert kind == "function"
    return list(parser.iter_values())


@pytest.mark.parametrize(
    "file_a, file_b, genome_length_b, expected",
    [
        pytest.param(
            "sample_function_a.f",
            "sample_function.csv",
            None,
            0.9022436386781062,
            id="function_vs_csv -> corr≈0.90 (strong positive)",
        ),
        pytest.param(
            "sample_function_a.f",
            "sample_function.const",
            "auto",
            math.nan,
            id="function_vs_const -> undefined correlation (NaN)",
        ),
    ],
)
def test_corr_supported_formats(file_a, file_b, genome_length_b, expected):
    values_a = _values(DATA_DIR / file_a)
    effective_length = len(values_a) if genome_length_b == "auto" else genome_length_b
    values_b = _values(DATA_DIR / file_b, genome_length=effective_length)
    result = pearson_correlation(values_a, values_b)
    if math.isnan(expected):
        assert math.isnan(result)
    else:
        assert pytest.approx(expected, rel=1e-12) == result


def test_corr_length_mismatch(tmp_path):
    """Mismatch in series length should raise to highlight data issues."""

    first = tmp_path / "short.f"
    second = tmp_path / "long.f"
    first.write_text("\n".join(["1.0", "2.0"]) + "\n", encoding="utf-8")
    second.write_text("\n".join(["1.0", "2.0", "3.0"]) + "\n", encoding="utf-8")
    with pytest.raises(ValueError):
        pearson_correlation(_values(first), _values(second))
