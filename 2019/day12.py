import re
import sys
from copy import deepcopy
from math import lcm
from pathlib import Path


def ints_in_str(s: str) -> list[int]:
    return [int(x) for x in re.findall(r"(-?\d+)", s)]


def calculate_energy_per_moon(moon_positions, moon_velocities):
    energy_per_moon = []
    for i in range(4):
        pot = sum(abs(x) for x in moon_positions[i])
        kin = sum(abs(x) for x in moon_velocities[i])
        energy_per_moon.append(pot * kin)
    return energy_per_moon


def part_one(moon_positions: list[tuple[int, ...]]) -> int:
    moon_velocities = [[0, 0, 0] for _ in range(len(moon_positions))]
    for _ in range(1000):
        new_positions = []
        for i in range(len(moon_positions)):

            for j in range(len(moon_positions)):
                if i == j:
                    continue
                for k in range(3):
                    if moon_positions[i][k] > moon_positions[j][k]:
                        moon_velocities[i][k] -= 1
                    elif moon_positions[i][k] < moon_positions[j][k]:
                        moon_velocities[i][k] += 1

            new_positions.append([p + v for p, v in zip(moon_positions[i], moon_velocities[i])])
        moon_positions = new_positions
    return sum(calculate_energy_per_moon(moon_positions, moon_velocities))


def part_two(moon_positions: list[tuple[int, ...]]) -> int:
    step_repeat = []
    for axis in range(3):
        axis_velocity = [0 for _ in range(len(moon_positions))]
        axis_positions = [moon_positions[i][axis] for i in range(len(moon_positions))]

        step = 1
        while True:
            for i, p1 in enumerate(axis_positions):
                for p2 in axis_positions:
                    if p1 == p2:
                        continue
                    if p1 > p2:
                        axis_velocity[i] -= 1
                    else:
                        axis_velocity[i] += 1
            new_axis_poses = [p + v for p, v in zip(axis_positions, axis_velocity)]

            is_first = all(moon_positions[i][axis] == new_axis_poses[i] for i in range(len(moon_positions)))
            velocities_zero = all(v == 0 for v in axis_velocity)
            if is_first and velocities_zero:
                step_repeat.append(step)
                break

            axis_positions = new_axis_poses
            step += 1
    return lcm(*step_repeat)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"

    moon_positions = []
    for line in input_path.read_text().splitlines():
        moon_positions.append(ints_in_str(line))

    print("FIRST PART", part_one(deepcopy(moon_positions)))
    print("SECOND PART", part_two(moon_positions))
