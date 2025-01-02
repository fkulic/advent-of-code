import re
import sys
from pathlib import Path


def ints_in_str(s: str) -> list[int]:
    return [int(x) for x in re.findall(r"(-?\d+)", s)]


def fuel_needed(module_mass: int):
    return module_mass // 3 - 2


def part_one(mass_modules: list[int]) -> int:
    return sum(fuel_needed(mass) for mass in mass_modules)


def part_two(mass_modules: list[int]) -> int:
    s = 0
    for mass in mass_modules:
        m = mass
        while (fuel := fuel_needed(m)) > 0:
            s += fuel
            m = fuel
    return s


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"
    data = ints_in_str(input_path.read_text())

    print("FIRST PART", part_one(data))
    print("SECOND PART", part_two(data))
