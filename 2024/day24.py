import sys
from pathlib import Path


def execute(values: dict[str, int], operations: dict[str, tuple[str, str, str]]) -> None:
    executed = set()
    while len(executed) != len(operations):
        for k in set(operations.keys()) - executed:
            in1, in2, op = operations[k]
            if k not in executed and in1 in values and in2 in values:
                executed.add(k)
                in1 = values[in1]
                in2 = values[in2]
                r = None
                match op:
                    case "AND":
                        r = in1 & in2
                    case "OR":
                        r = in1 | in2
                    case "XOR":
                        r = in1 ^ in2
                assert r is not None
                values[k] = r


def part_one(values: dict[str, int], operations: dict[str, tuple[str, str, str]]) -> int:
    execute(values, operations)
    out = 0
    for k, v in values.items():
        if k.startswith("z"):
            out += v << int(k.split("z")[-1])
    return out


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"

    initial_values, operation_lines = input_path.read_text().strip().split("\n\n")

    values = {}
    for iv_line in initial_values.splitlines():
        k, v = iv_line.split(": ")
        values[k] = int(v)

    operations = {}
    for op_line in operation_lines.splitlines():
        in1, op, in2, _, out = op_line.split(" ")
        operations[out] = (in1, in2, op)

    print("FIRST PART", part_one(values, operations))
    # print("SECOND PART", part_two(values, operations))
