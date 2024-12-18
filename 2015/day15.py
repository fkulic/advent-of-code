import re
import sys
from functools import reduce
from operator import mul
from pathlib import Path
from typing import Generator


def ints_in_str(s: str) -> list[int]:
    return [int(x) for x in re.findall(r"(-?\d+)", s)]


def get_combinations(n: int, total: int) -> Generator[list[int]]:
    assert n > 0
    if n == 1:
        yield [total]
    else:
        for i in range(total + 1):
            for rest in get_combinations(n - 1, total - i):
                yield [i] + rest


def calc_score(score_per_property: list[int]) -> int:
    if 0 in score_per_property:
        return 0
    return reduce(mul, score_per_property, 1)


def part_one(ingredients: list[list[int]]) -> int:
    max_s = 0
    for c in get_combinations(len(ingredients), 100):
        s = [0 for _ in range(len(ingredients[0]))]
        for i, ing in enumerate(ingredients):
            for j in range(len(ing)):
                s[j] += c[i] * ing[j]
        for i in range(len(s)):
            if s[i] < 0:
                s[i] = 0
        max_s = max(calc_score(s), max_s)
    return max_s


def part_two(ingredients: list[list[int]], calories: list[int], wanted_cals: int = 500) -> int:
    max_s = 0
    for c in get_combinations(len(ingredients), 100):
        s = [0 for _ in range(len(ingredients[0]))]
        cals = 0
        for i, ing in enumerate(ingredients):
            cals += c[i] * calories[i]
            for j in range(len(ing)):
                s[j] += c[i] * ing[j]
        if cals != wanted_cals:
            continue
        for i in range(len(s)):
            if s[i] < 0:
                s[i] = 0
        max_s = max(calc_score(s), max_s)
    return max_s


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"
    data = input_path.read_text().strip()

    ingredients = []
    calories = []
    for l in data.splitlines():
        nums = ints_in_str(l)
        ingredients.append(nums[:-1])
        calories.append(nums[-1])

    print("FIRST PART", part_one(ingredients))
    print("SECOND PART", part_two(ingredients, calories))
