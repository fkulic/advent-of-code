import operator
from pathlib import Path
import re
import sys


def ints_in_str(s: str) -> list[int]:
    return [int(x) for x in re.findall(r"(-?\d+)", s)]


def call_operator(numbers, op, r=None):
    if r == None:
        if op == operator.add:
            r = 0
        else:
            r = 1
    if len(numbers) == 0:
        return r

    return call_operator(numbers[1:], op, op(r, numbers[0]))


def part_one(data: list[str]) -> int:
    ops = []
    for c in data[-1]:
        if c == "*":
            ops.append(operator.mul)
        elif c == "+":
            ops.append(operator.add)

    numbers = []
    for row in data[:-1]:
        numbers.append(ints_in_str(row))

    transformed = []
    for i in range(len(ops)):
        col = []
        for row in numbers:
            col.append(row[i])
        transformed.append(col)

    total_sum = 0
    for i in range(len(ops)):
        total_sum += call_operator(transformed[i], ops[i])
    return total_sum


def part_two(data: list[str]) -> int:
    ops = []
    for c in data[-1]:
        if c == "*":
            ops.append(operator.mul)
        elif c == "+":
            ops.append(operator.add)

    all = []
    res = 0
    op = operator.add
    for c in range(len(data[0])):
        match data[-1][c]:
            case "*":
                res = 1
                op = operator.mul
            case "+":
                res = 0
                op = operator.add

        n = ""
        for r in range(len(data[:-1])):
            if data[r][c] != " ":
                n += data[r][c]

        if n == "":
            all.append(res)
        else:
            res = op(res, int(n))
    all.append(res)

    return sum(all)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    if not input_path.is_file():
        print(f"{input_path} is not a file")
        sys.exit(1)

    data = input_path.read_text().split("\n")[:-1]

    print("FIRST PART", part_one(data))
    print("SECOND PART", part_two(data))
