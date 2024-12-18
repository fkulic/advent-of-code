import operator
import re
import sys
from collections import Counter
from pathlib import Path


def part_one(sue_data: str, mfcsam_data: list[str]) -> int:
    c = Counter()
    for d in mfcsam_data:
        m = re.findall(r"Sue (\d+).*" + d, sue_data)
        c.update(m)
    return c.most_common(1)[0][0]


def part_two(sue_data: str, mfcsam_data: list[str]) -> int:
    parsed_mfcsam_data = {}
    for line in mfcsam_data:
        thing, count = line.strip().split(": ")
        parsed_mfcsam_data[thing] = int(count)

    ops = {
        "cats": operator.gt,
        "trees": operator.gt,
        "pomeranians": operator.lt,
        "goldfish": operator.lt,
    }

    c = Counter()
    for thing, count in parsed_mfcsam_data.items():
        op = ops.get(thing, operator.eq)
        for m in re.findall(f"Sue (\\d+).*{thing}: (\\d+).*\n", sue_data):
            sue_n, thing_c = m
            if op(int(thing_c), count):
                c[sue_n] += 1
    return c.most_common(1)[0][0]


if __name__ == "__main__":
    assert len(sys.argv) > 2, "No input paths"

    input_path = Path(sys.argv[1])
    assert input_path.is_file(), "Not file"

    mfcsam_output = Path(sys.argv[2])
    assert input_path.is_file(), "Not file. Needs to be path to output from MFCSAM"

    sue_data = input_path.read_text().strip()
    mfcsam_data = mfcsam_output.read_text().strip().splitlines()

    print("FIRST PART", part_one(sue_data, mfcsam_data))
    print("SECOND PART", part_two(sue_data, mfcsam_data))
