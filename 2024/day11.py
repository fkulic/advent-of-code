import sys
from functools import cache
from math import log10
from pathlib import Path


def split(s: int) -> tuple[int | int] | None:
    n = int(log10(s)) + 1
    if n % 2 == 0:
        d = 10 ** (n // 2)
        left = s // d
        right = s - left * d
        return left, right
    return False


@cache
def blink_n(s: int, n: int) -> int:
    if n == 0:
        return 1
    if s == 0:
        ret = blink_n(1, n - 1)
    elif splitted_s := split(s):
        ret = blink_n(splitted_s[0], n - 1) + blink_n(splitted_s[1], n - 1)
    else:
        ret = blink_n(2024 * s, n - 1)
    return ret


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    stones = [int(x) for x in input_path.read_text().strip().split()]

    print("FIRST PART", sum(blink_n(s, 25) for s in stones))
    print("SECOND PART", sum(blink_n(s, 75) for s in stones))
