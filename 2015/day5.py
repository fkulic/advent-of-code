import sys
from collections import defaultdict
from pathlib import Path


def part_one(data: list[str]) -> int:
    nice = 0
    for s in data:
        vowels_c = 0
        twice = False
        contains_s = False
        for i, c in enumerate(s):
            if c in "aeiou":
                vowels_c += 1
            if i < len(s) - 1:
                if not twice and c == s[i + 1]:
                    twice = True
                if s[i : i + 2] in ("ab", "cd", "pq", "xy"):
                    contains_s = True
                    break
        if not contains_s and twice and vowels_c >= 3:
            nice += 1
    return nice


def part_two(data: list[str]) -> int:
    nice = 0
    for s in data:
        rule1 = False
        rule2 = False
        not_nice = False
        pairs = defaultdict(int)
        pairs[s[-2:]] += 1
        for i in range(2, len(s)):
            if s[i - 2] == s[i] and s[i] != s[i - 1]:
                rule2 = True
            if s[i - 2] == s[i] and s[i - 1] == s[i]:
                not_nice = True
                break
            pairs[s[i - 2 : i]] += 1

        for c in pairs.values():
            if c > 1:
                rule1 = True
                break
        if not not_nice and rule1 and rule2:
            nice += 1

    return nice


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"
    data = input_path.read_text().strip().splitlines()

    print("FIRST PART", part_one(data))
    print("SECOND PART", part_two(data))
