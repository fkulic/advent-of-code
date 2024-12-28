import sys
from copy import deepcopy
from dataclasses import dataclass
from itertools import product
from pathlib import Path

from rich.live import Live
from rich.table import Table


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def is_inside(self, dimensions: "Point") -> bool:
        return 0 <= self.x < dimensions.x and 0 <= self.y < dimensions.y


AROUND = [Point(x, y) for x, y in product([0, -1, 1], repeat=2) if x != 0 or y != 0]


def step(lights, always_on=()) -> None:
    changes = {}
    for i, line in enumerate(lights):
        for j, light in enumerate(line):
            p = Point(i, j)
            if p in always_on:
                continue
            around_on = sum(1 for a in AROUND if (ap := p + a).is_inside(DIMENSIONS) and lights[ap.x][ap.y] == "#")
            if light == "#":
                if around_on not in (2, 3):
                    changes[p] = "."
            elif around_on == 3:
                changes[p] = "#"
    for p, new_light in changes.items():
        lights[p.x][p.y] = new_light


def create_visualize_lights_table(lights):
    table = Table(show_header=False)
    for row in lights:
        table.add_row("".join(row))
    return table


def part_one(lights: list[list[str]]) -> int:
    with Live(create_visualize_lights_table(lights)) as live:
        for _ in range(100):
            step(lights)
            live.update(create_visualize_lights_table(lights), refresh=True)

    return sum(1 for line in lights for l in line if l == "#")


def part_two(lights: list[list[str]]) -> int:
    always_on = (
        Point(0, 0),
        Point(DIMENSIONS.x - 1, 0),
        Point(0, DIMENSIONS.y - 1),
        Point(DIMENSIONS.x - 1, DIMENSIONS.y - 1),
    )
    for p in always_on:
        lights[p.x][p.y] = "#"

    with Live(create_visualize_lights_table(lights)) as live:
        for _ in range(100):
            step(lights, always_on)
            live.update(create_visualize_lights_table(lights), refresh=True)

    return sum(1 for line in lights for l in line if l == "#")


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"

    input_path = Path(sys.argv[1])
    assert input_path.is_file(), "Not file"

    lights = [list(line) for line in input_path.read_text().splitlines()]
    DIMENSIONS = Point(len(lights), len(lights[0]))

    print("FIRST PART", part_one(deepcopy(lights)))
    print("SECOND PART", part_two(lights))
