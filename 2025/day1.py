import sys
from pathlib import Path


def part_one(sequence: list[int]) -> int:
    pos = 50
    total_at_0 = 0
    for instruction in sequence:
        pos += instruction
        pos %= 100
        if pos == 0:
            total_at_0 += 1
    return total_at_0


def part_two(sequence: list[int]) -> int:
    pos = 50
    total_at_0 = 0
    for instruction in sequence:
        new_pos = pos + instruction
        if instruction >= 0:
            total_at_0 += new_pos // 100
        else:
            if pos == 0:
                total_at_0 += abs(instruction) // 100
            else:
                total_at_0 += 1 + -new_pos // 100
        pos = new_pos % 100
    return total_at_0


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    if not input_path.is_file():
        print(f"{input_path} is not a file")
        sys.exit(1)

    sequence = []
    for line in input_path.read_text().splitlines():
        if line.startswith("L"):
            sequence.append(-int(line[1:]))
        else:
            sequence.append(int(line[1:]))

    print("FIRST PART", part_one(sequence))
    print("SECOND PART", part_two(sequence))
