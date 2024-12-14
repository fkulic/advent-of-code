import operator
import sys
from collections import defaultdict
from functools import reduce
from pathlib import Path

import numpy as np
from PIL import Image

ROWS, COLS = 103, 101
HALF_R = ROWS // 2
HALF_C = COLS // 2

IMAGES_DIR = Path(__file__).parent / f"day14_trees"


def get_map() -> list[list[int]]:
    return [[0 for _ in range(COLS)] for __ in range(ROWS)]


def safety_factor(robot_positions: dict[tuple[int, int], int]) -> int:
    counts = [[0, 0], [0, 0]]
    for (x, y), c in robot_positions.items():
        if x == HALF_R or y == HALF_C:
            continue
        counts[int(x > HALF_R)][int(y > HALF_C)] += c

    return reduce(operator.mul, [c for cs in counts for c in cs], 1)


def first_part(data: list[str]) -> int:
    seconds = 100
    robot_positions = defaultdict(int)
    for line in data:
        left, right = line.strip().split()
        y, x = [int(v) for v in left.split("=")[1].split(",")]
        dy, dx = [int(v) for v in right.split("=")[1].split(",")]
        y = (y + seconds * dy) % COLS
        x = (x + seconds * dx) % ROWS
        robot_positions[(x, y)] += 1

    return safety_factor(robot_positions)


def second_part(data: list[str]) -> str:
    values = []
    for line in data:
        left, right = line.strip().split()
        y, x = [int(v) for v in left.split("=")[1].split(",")]
        dy, dx = [int(v) for v in right.split("=")[1].split(",")]
        values.append([x, y, dx, dy])

    s = 0
    for i in range(1, 10000):
        s += 1
        for i, v in enumerate(values):
            x, y, dx, dy = v
            y = (y + dy) % COLS
            x = (x + dx) % ROWS
            values[i][0] = x
            values[i][1] = y

        # Dumb solution, robot positions white and save 10000 images
        map = get_map()
        for x, y, dx, dy in values:
            map[x][y] = 255

        grayscale_array = np.array(map, dtype=np.uint8)
        image = Image.fromarray(grayscale_array, mode="L")
        image.save(
            IMAGES_DIR / f"{s}.png",
            bbox_inches="tight",
            pad_inches=0,
        )

    return f"Look through images, I have no idea how tree looks like: {IMAGES_DIR.absolute()}"


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    data: list[str] = input_path.read_text().strip().splitlines()

    print("FIRST PART", first_part(data))
    print("SECOND PART", second_part(data))
