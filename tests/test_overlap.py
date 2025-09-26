from pathlib import Path
import pytest

from elixir_task.analysis import overlap_length
from elixir_task.registry import guess_parser

DATA_DIR = Path(__file__).parent / "data"


def _segments(path: Path):
    kind, parser = guess_parser(path)
    assert kind == "segment"
    return list(parser.iter_segments())


@pytest.mark.parametrize(
    "segment_file_a, segment_file_b, expected",
    [
        pytest.param(
            "sample_segments_a.s",
            "sample_segments_b.s",
            3,
            id="SEGMENT(.s) vs SEGMENT(.s) -> shared length 3",
        ),
        pytest.param(
            "sample_segments_a.s",
            "sample_segments.bed",
            2,
            id="SEGMENT(.s) vs SEGMENT(.bed) -> shared length 2",
        ),
    ],
)
def test_overlap_supported_formats(segment_file_a, segment_file_b, expected):
    first = _segments(DATA_DIR / segment_file_a)
    second = _segments(DATA_DIR / segment_file_b)
    result = overlap_length(first, second)
    assert result == expected


def test_overlap_disjoint(tmp_path):
    """Adjacent segments with no shared bases should yield zero overlap."""

    left = tmp_path / "left.s"
    right = tmp_path / "right.s"
    left.write_text("0\t5\n", encoding="utf-8")
    right.write_text("5\t8\n", encoding="utf-8")
    result = overlap_length(_segments(left), _segments(right))
    assert result == 0
