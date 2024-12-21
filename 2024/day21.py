from collections import defaultdict, deque
from dataclasses import dataclass
from functools import cache
import sys
from pathlib import Path

sys.setrecursionlimit(10**6)

GAP = (3, 0)
numeric_dimensions = (4, 3)
numeric_mapping = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}


def get_numeric_combination(combination: str, c_button: str = "A") -> str:
    if len(combination) == 0:
        return ""
    c_pos = numeric_mapping[c_button]
    next_button = combination[0]
    next_pos = numeric_mapping[next_button]

    out = []
    dx, dy = next_pos[0] - c_pos[0], next_pos[1] - c_pos[1]
    if c_pos[0] == 3 and next_pos[1] == 0:
        out += ["^" for _ in range(abs(dx))]
        out += ["<" for _ in range(abs(dy)) if dy < 0]
    elif c_pos[1] == 0 and next_pos[0] == 3:
        out += [">" for _ in range(abs(dy))]
        out += ["v" for _ in range(abs(dx)) if dx > 0]
    elif dy < 0:
        out += ["<" for _ in range(abs(dy))]
        out += ["^" for _ in range(abs(dx)) if dx < 0]
        out += ["v" for _ in range(abs(dx)) if dx > 0]
    else:
        out += ["^" for _ in range(abs(dx)) if dx < 0]
        out += ["v" for _ in range(abs(dx)) if dx > 0]
        out += [">" for _ in range(abs(dy))]

    out.append("A")
    return "".join(out) + get_numeric_combination(combination[1:], next_button)


GAP = (0, 0)
directional_dimensions = (2, 3)
directional_mapping = {
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}


@cache
def reverse(combination) -> str:
    Q = deque(combination)
    l = []
    while Q:
        n = Q.pop()
        match n:
            case "^":
                l.append("v")
            case "<":
                l.append(">")
            case "v":
                l.append("^")
            case ">":
                l.append("<")
    return "".join(l)


@cache
def _get_directional_combination(to_button: str, from_button: str = "A"):
    c_pos = directional_mapping[from_button]
    next_pos = directional_mapping[to_button]

    dx, dy = next_pos[0] - c_pos[0], next_pos[1] - c_pos[1]
    out = []
    if from_button == "<":
        out += [">" for _ in range(abs(dy))]
        out += ["^" for _ in range(abs(dx))]
    elif to_button == "<":
        out += ["v" for _ in range(abs(dx))]
        out += ["<" for _ in range(abs(dy))]
    elif dy < 0:
        out += ["<" for _ in range(abs(dy))]
        out += ["^" for _ in range(abs(dx)) if dx < 0]
        out += ["v" for _ in range(abs(dx)) if dx > 0]
    else:
        out += ["^" for _ in range(abs(dx)) if dx < 0]
        out += ["v" for _ in range(abs(dx)) if dx > 0]
        out += [">" for _ in range(abs(dy))]

    comb = "".join(out)
    return f"{comb}A"


def get_directional_combination(combination: str, last="A"):
    if len(combination) == 0:
        return ""

    current = combination[0]
    return _get_directional_combination(current, last) + get_directional_combination(combination[1:], current)


def part_one(data: list[str]) -> int:
    res = []
    for i, comb in enumerate(data):
        n_comb = get_numeric_combination(comb)
        for _ in range(2):
            n_comb = get_directional_combination(n_comb)
        res.append((len(n_comb), int(comb[:-1])))
    print(res)
    return sum(c * n for c, n in res)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"
    data = input_path.read_text().strip().splitlines()

    print("FIRST PART", part_one(data))
