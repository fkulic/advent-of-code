import re
import sys
from collections import deque
from copy import deepcopy
from math import ceil
from pathlib import Path

from intcode import IntCodeComputer


def ints_in_str(s: str) -> list[int]:
    return [int(x) for x in re.findall(r"(-?\d+)", s)]


class Solution:
    def __init__(self, memory: list[int]) -> None:
        self._memory = memory
        self._q = deque([])

    def _in_function(self):
        x = self._q.popleft()
        return x

    def is_being_pulled(self, row, col) -> int:
        self._q.append(row)
        self._q.append(col)
        computer = IntCodeComputer(deepcopy(self._memory), self._in_function)
        computer.run_intcode()
        return computer.output[-1]

    def get_left(self, row, left_k) -> int:
        left = int(row / left_k) - 1
        while self.is_being_pulled(row, left) == 0:
            left += 1
            if left > row:
                return 0
        return left

    def can_fit_box(self, row, left, n) -> bool:
        up_row = row - n + 1
        right_col = left + n - 1
        for i in range(n):
            if not self.is_being_pulled(up_row + i, right_col):
                return False
            if not self.is_being_pulled(row - i, left):
                return False
        return True


def part_one(memory: list[int]) -> int:
    solution = Solution(memory)
    total = 1
    for row in range(1, 50):
        left = row
        row_count = 0
        while True:
            val = solution.is_being_pulled(row, left)
            row_count += val
            if row_count > 0:
                if val == 0:
                    break
            elif row - left > 5:
                break
            left -= 1
        total += row_count
    return total


def part_two(memory: list[int]) -> int:
    solution = Solution(memory)
    row = 1
    row_count = 0
    first, second_l = None, None
    while second_l is None:
        row += 1
        left = row
        row_count = 0
        while True:
            val = solution.is_being_pulled(row, left)
            row_count += val
            if row_count == 1 and val == 1 and first is None:
                first = row, left
            elif row_count == 2 and second_l is None:
                second_l = row, left
            elif row_count > 0 and val == 0 or left == 0:
                break
            left -= 1

    assert first is not None and second_l is not None
    left_k = (second_l[0] - first[0]) / (second_l[1] - first[1])

    backtrack = None
    box_side = 100
    row, increment = box_side, box_side
    while True:
        left = solution.get_left(row, left_k)
        can_fit = solution.can_fit_box(row, left, box_side)

        if can_fit and backtrack is not False:
            if increment == 1:
                return (row - box_side + 1) * 10000 + left
            backtrack = False
            increment = int(ceil(-increment / 2))

        elif not can_fit and backtrack is False:
            backtrack = True
            increment = int(ceil(-increment / 2))

        row += increment


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"

    memory = ints_in_str(input_path.read_text())

    print("FIRST PART", part_one(memory))
    print("SECOND PART", part_two(memory))
