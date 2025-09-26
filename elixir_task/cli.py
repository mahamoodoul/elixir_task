from __future__ import annotations
import argparse
from pathlib import Path
from .registry import guess_parser
from .models import SegmentSource, FunctionSource
from .analysis import overlap_length, pearson_correlation, covered_mean

def main(argv=None):
    p = argparse.ArgumentParser(description="ELIXIR 2025 Task CLI")
    p.add_argument('file_x', type=Path)
    p.add_argument('file_y', type=Path)
    p.add_argument('--genome-length', type=int, default=None, help='Required for .const function files')
    p.add_argument('--output', type=Path, default=None, help='Optional output file to write result')
    args = p.parse_args(argv)

    kind_x, parser_x = guess_parser(args.file_x, genome_length=args.genome_length)
    kind_y, parser_y = guess_parser(args.file_y, genome_length=args.genome_length)

    # Decide operation by kinds
    if kind_x == 'segment' and kind_y == 'segment':
        res = overlap_length(parser_x.iter_segments(), parser_y.iter_segments())
    elif kind_x == 'function' and kind_y == 'function':
        res = pearson_correlation(parser_x.iter_values(), parser_y.iter_values())
    elif kind_x == 'segment' and kind_y == 'function':
        res = covered_mean(parser_x.iter_segments(), parser_y.iter_values())
    elif kind_x == 'function' and kind_y == 'segment':
        res = covered_mean(parser_y.iter_segments(), parser_x.iter_values())
    else:
        raise RuntimeError('Unsupported combination')

    if args.output:
        args.output.write_text(str(res) + "\n", encoding='utf-8')
    else:
        print(res)

if __name__ == '__main__':
    main()
