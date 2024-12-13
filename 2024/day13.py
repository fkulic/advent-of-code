import re
import sys
from pathlib import Path


def solve(xa, ya, xb, yb, xx, yy) -> tuple[int, int] | None:
    # ta*xa+tb*xb=xx
    # ta*ya+tb*yb=yy
    tb = (xx * ya - yy * xa) // (ya * xb - yb * xa)
    ta = (xx - tb * xb) // xa
    if ta * xa + tb * xb == xx and ta * ya + tb * yb == yy:
        return ta, tb
    return None


def first_part(equations: list[list[int]]) -> int:
    total_cost = 0
    for e in equations:
        t = solve(*e)
        if t and t[0] <= 100 and t[1] <= 100:
            total_cost += 3 * t[0] + t[1]
    return total_cost


def second_part(equations: list[list[int]]) -> int:
    total_cost = 0
    for e in equations:
        xa, ya, xb, yb, xx, yy = e
        xx += 10000000000000
        yy += 10000000000000
        t = solve(xa, ya, xb, yb, xx, yy)
        if t:
            total_cost += 3 * t[0] + t[1]
    return total_cost


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    data: list[str] = input_path.read_text().strip().split("\n\n")

    commands = []
    re_pattern = re.compile(r"\w+ A: X\+(\d+).*Y\+(\d+)\n\w+ B: X\+(\d+).*Y\+(\d+)\n\w+: X=(\d+), Y=(\d+)")

    equations = []
    for machine in data:
        match = re_pattern.match(machine)
        equations.append([int(g) for g in match.groups()])

    print("FIRST PART", first_part(equations))
    print("SECOND PART", second_part(equations))
