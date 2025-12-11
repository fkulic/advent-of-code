from copy import deepcopy
import heapq
import random
import re
import sys
from collections import Counter
from itertools import combinations_with_replacement
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor


def ints_in_str(s: str) -> list[int]:
    return [int(x) for x in re.findall(r"(-?\d+)", s)]

def part_one(machine_data) -> int:
    total = 0
    for indicators, buttons, _ in machine_data:
        expected_result = 0
        min_score = 10000
        for i in range(len(indicators)):
            expected_result += (2**i) * int(indicators[i] == "#")
        
        buttons_as_ints = []
        for btns in buttons:
            buttons_as_ints.append(sum(2**b for b in btns))

        for combination in range(2**len(buttons)):
            pushed = 0
            current_status = 0
            for i in range(len(buttons)):
                if (combination >> i) & 1 == 1:
                    current_status ^= buttons_as_ints[i]
                    pushed +=1
                if current_status == expected_result:
                    min_score = min(min_score, pushed)
        total += min_score
    return total


def push_button_joltage(joltage, button):
    for b in button:
        joltage[b] += 1


def push_joltage_buttons_until_equals(joltage, buttons, min_achieved=100000):
    n = 0
    current_joltage = [0 for _ in range(len(joltage))]
    while True:
        n += 1
        if n > min_achieved:
            return min_achieved

        push_button_joltage(current_joltage, random.choice(buttons))

        equals = True
        for j1, j2 in zip(current_joltage, joltage):
            if j1 > j2:
                return min_achieved
            elif j1 < j2:
                equals = False

        if equals:
            return n

        if n > min_achieved:
            return min_achieved


def compare_joltage(current, expected):
    how_many_different = 0
    for j1, j2 in zip(current, expected):
        if j1 > j2:
            return -1
        elif j1 < j2:
            how_many_different += 1
    return how_many_different


def push_combination_joltage(joltage, buttons):
    new_joltage = deepcopy(joltage)
    c = Counter([x for button in buttons for x in button])
    for b, o in c.items():
        new_joltage[b] += o
    return new_joltage


def get_least_common_that_needs_pressing(
    counted_buttons, current_joltage, expected_joltage
):
    for b, _ in reversed(counted_buttons.items()):
        if expected_joltage[b] > current_joltage[b]:
            return b

def get_new_combination(button, counted_buttons, r):
    for c in random.shuffle(combinations_with_replacement(len(counted_buttons), r)):
        yield c

def try_number_9881(buttons, joltage):
    print(buttons)
    counted_buttons = Counter([x for button in buttons for x in button])
    buttons_map = {i: [b for b in buttons if i in b] for i in range(len(joltage))}
    for i in range(len(buttons_map)):
        buttons_map[i].sort(key=len, reverse=True)

    # buttons = [[int(i in btns) for i in range(len(joltage))] for btns in buttons]
    starting_joltage = [0 for _ in range(len(joltage))]
    for b, _ in reversed(counted_buttons.items()):
        b_combination = get_new_combination(b, counted_buttons, joltage[b] - starting_joltage[b])
        for asd in b_combination:
            print(asd)

        pass
    print(joltage)
    print(buttons)

def part_two(machine_data) -> int:
    return 2
    total = 0
    # with ProcessPoolExecutor() as executor:
    #     return sum(executor.map(joltage_min_in_n_times, machine_data))
    for _, buttons, joltage in machine_data:
        counted_buttons = Counter([x for button in buttons for x in button])
        starting_joltage = [0 for _ in range(len(joltage))]
        heap = [(0, starting_joltage, 0)]
        min_preses = [1000]
        while heap:
            if len(min_preses) > 10:
                break

            _, current_joltage, current_presses = heapq.heappop(heap)
            if current_presses > min_preses[0]:
                continue

            least_common = get_least_common_that_needs_pressing(
                counted_buttons, current_joltage, joltage
            )
            if least_common is None:
                continue

            p = [b for b in buttons if least_common in b]
            r = joltage[least_common] - current_joltage[least_common]

            for button_combination in combinations_with_replacement(p, r):
                new_joltage = push_combination_joltage(
                    current_joltage, button_combination
                )
                new_presses = current_presses + r
                compare_result = compare_joltage(new_joltage, joltage)
                if compare_result == 0:
                    heapq.heappush(min_preses, new_presses)
                elif compare_result > 0:
                    heapq.heappush(heap, (compare_result, new_joltage, new_presses))
                    if len(heap) % 100 == 0:
                        print(len(heap))
        total += min(min_preses)
        print(min_preses)

    return total


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    if not input_path.is_file():
        print(f"{input_path} is not a file")
        sys.exit(1)

    machine_data = []
    for line in input_path.read_text().strip().splitlines():
        indicators, other = line.split("]")
        indicators = indicators[1:]
        buttons, joltage = other.split("{")
        buttons = [set(ints_in_str(button)) for button in buttons.split()]
        joltage = ints_in_str(joltage)
        machine_data.append((indicators, buttons, joltage))

    print("FIRST PART", part_one(machine_data))
    # print("SECOND PART", part_two(machine_data))
