import sys
from collections import Counter
from functools import cache
from pathlib import Path

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


def _get_numeric_combination(to_button: str, from_button: str = "A") -> str:
    c_pos = numeric_mapping[from_button]
    next_pos = numeric_mapping[to_button]

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
    return "".join(out)


def get_numeric_combination(combination: str):
    dpad_combinations = []
    for i, buton in enumerate(combination):
        if i == 0:
            dpad_combinations.append(_get_numeric_combination(buton))
        else:
            dpad_combinations.append(_get_numeric_combination(buton, combination[i - 1]))
    return Counter(dpad_combinations)


directional_dimensions = (2, 3)
directional_mapping = {
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}


@cache
def dpad_combination_between_buttons(to_button: str, from_button: str = "A"):
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


DPAD_CACHE = {}
def _get_directional_combination(combination: str, last="A"):
    if len(combination) == 0:
        return ""

    if combination in DPAD_CACHE:
        return DPAD_CACHE[combination]

    new_dpad_combination = []
    for i, buton in enumerate(combination):
        if i == 0:
            new_dpad_combination.append(dpad_combination_between_buttons(buton))
        else:
            new_dpad_combination.append(dpad_combination_between_buttons(buton, combination[i - 1]))

    DPAD_CACHE[combination] = new_dpad_combination

    return new_dpad_combination


def get_directional_combination(combinations: Counter[str]):
    new_combinations = Counter()
    for dpad_comb, count in combinations.items():
        for combination in _get_directional_combination(dpad_comb):
            new_combinations[combination] += count

    return new_combinations


def both_parts(data: list[str]) -> tuple[int, int]:
    first = 0
    second = 0
    for i, comb in enumerate(data):
        num_input = int(comb[:-1])
        n_comb = get_numeric_combination(comb)
        for i in range(25):
            n_comb = get_directional_combination(n_comb)
            if i == 1:
                total_len = sum(len(dpad_combination) * count for dpad_combination, count in n_comb.items())
                first += total_len * num_input
        total_len = sum(len(dpad_combination) * count for dpad_combination, count in n_comb.items())
        second += total_len * num_input
    return first, second


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"
    data = input_path.read_text().strip().splitlines()

    first, second = both_parts(data)
    print("FIRST PART", first)
    print("SECOND PART", second)
