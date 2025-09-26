def to_float(s: str) -> float:
    value = s.strip()
    if not value:
        raise ValueError("Encountered empty value while parsing float")
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(f"Could not parse float from {value!r}") from exc


def to_int(s: str) -> int:
    value = s.strip()
    if not value:
        raise ValueError("Encountered empty value while parsing int")
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"Could not parse int from {value!r}") from exc


def safe_strip(line: str) -> str:
    return line.rstrip("\n\r")
