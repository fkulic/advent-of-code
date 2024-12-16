import sys
from collections import defaultdict
from itertools import permutations
from pathlib import Path


def happies_arrangment(invitees_data: dict[str, dict[str, int]]) -> int:
    max_happy = 0
    for per in permutations(invitees_data):
        happines = 0
        for i, p in enumerate(per):
            other = per[(i + 1) % len(per)]
            happines += invitees_data[p][other] + invitees_data[other][p]
        max_happy = max(happines, max_happy)
    return max_happy


def part_one(invitees_data: dict[str, dict[str, int]]) -> int:
    return happies_arrangment(invitees_data)


def part_two(invitees_data: dict[str, dict[str, int]]) -> int:
    for name in list(invitees_data.keys()):
        invitees_data[name]["Me"] = 0
        invitees_data["Me"][name] = 0
    return happies_arrangment(invitees_data)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"
    data = input_path.read_text().strip()

    invitees_data = defaultdict(dict)
    for line in data.splitlines():
        splitted = line[:-1].split()
        who = splitted[0]
        gain_or_lose, how_much = splitted[2:4]
        by_whom = splitted[-1]
        how_much = int(how_much) * (-1 if "lose" == gain_or_lose else 1)
        invitees_data[who][by_whom] = how_much

    print("FIRST PART", part_one(invitees_data))
    print("SECOND PART", part_two(invitees_data))
