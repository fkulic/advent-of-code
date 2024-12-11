import sys
from pathlib import Path


def part_one(data: list[int]) -> int:
    x, y = 0, 0
    visited = set([x, y])
    for c in data:
        match c:
            case "^":
                x -= 1
            case ">":
                y += 1
            case "v":
                x += 1
            case "<":
                y -= 1
        visited.add((x, y))
    return len(visited)


def part_two(data: str) -> int:
    pos = [[0, 0], [0, 0]]
    visited = set([(0, 0)])
    for i, c in enumerate(data):
        p = i % 2
        match c:
            case "^":
                pos[p][0] -= 1
            case ">":
                pos[p][1] += 1
            case "v":
                pos[p][0] += 1
            case "<":
                pos[p][1] -= 1
        visited.add((pos[p][0], pos[p][1]))
    return len(visited)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"
    data = input_path.read_text().strip()

    print("FIRST PART", part_one(data))
    print("SECOND PART", part_two(data))
