import math
from pathlib import Path
import pytest

from elixir_task.analysis import covered_mean
from elixir_task.registry import guess_parser

DATA_DIR = Path(__file__).parent / "data"


def _segments(path: Path):
    kind, parser = guess_parser(path)
    assert kind == "segment"
    return list(parser.iter_segments())


def _values(path: Path, genome_length: int | None = None):
    kind, parser = guess_parser(path, genome_length=genome_length)
    assert kind == "function"
    return list(parser.iter_values())


@pytest.mark.parametrize(
    "segment_file, function_file, genome_length_b, expected",
    [
        pytest.param(
            "sample_segments_a.s",
            "sample_function_b.f",
            None,
            12.0,
            id="SEGMENT(.s) + FUNCTION(.f) -> mean 12.0",
        ),
        pytest.param(
            "sample_segments.bed",
            "sample_function.csv",
            None,
            13.0,
            id="SEGMENT(.bed) + FUNCTION(.csv) -> mean 13.0",
        ),
        pytest.param(
            "sample_segments_a.s",
            "sample_function.const",
            6,
            3.5,
            id="SEGMENT(.s) + FUNCTION(.const) -> constant mean 3.5",
        ),
    ],
)
def test_mean_supported_formats(segment_file, function_file, genome_length_b, expected):
    segments = _segments(DATA_DIR / segment_file)
    values = _values(DATA_DIR / function_file, genome_length=genome_length_b)
    result = covered_mean(segments, values)
    assert pytest.approx(expected, rel=1e-12) == result


def test_mean_segment_exceeds_function(tmp_path):
    seg = tmp_path / "bad.s"
    func = tmp_path / "short.f"
    seg.write_text("5\t7\n", encoding="utf-8")
    func.write_text("\n".join(["1.0", "2.0", "3.0"]) + "\n", encoding="utf-8")
    result = covered_mean(_segments(seg), _values(func))
    assert math.isnan(result)
