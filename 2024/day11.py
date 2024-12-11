from collections import defaultdict
from pathlib import Path
from math import log10
import sys


def split(s: int) -> tuple[int | int] | None:
    n = int(log10(s)) + 1
    if n % 2 == 0:
        d = 10 ** (n // 2)
        left = s // d
        right = s - left * d
        return left, right
    return False


CACHE = defaultdict(dict)


def blink_n(s: int, n: int, c: int = 0) -> int:
    global CACHE
    if n == 0:
        return 1

    if x := CACHE.get(s, {}).get(c):
        return x

    if s == 0:
        ret = blink_n(1, n - 1, c + 1)
    elif splitted_s := split(s):
        ret = blink_n(splitted_s[0], n - 1, c + 1) + blink_n(splitted_s[1], n - 1, c + 1)
    else:
        ret = blink_n(2024 * s, n - 1, c + 1)
    CACHE[s][c] = ret
    return ret


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    stones = [int(x) for x in input_path.read_text().strip().split()]

    CACHE.clear()
    print("FIRST PART", sum(blink_n(s, 25) for s in stones))
    CACHE.clear()
    print("SECOND PART", sum(blink_n(s, 75) for s in stones))
