from typing import Optional

def to_float(s: str) -> float:
    s = s.strip()
    if not s:
        return 0.0
    return float(s)

def to_int(s: str) -> int:
    return int(s.strip())

def safe_strip(line: str) -> str:
    return line.rstrip("\n\r")
