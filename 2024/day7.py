import sys
from collections import defaultdict
from itertools import product
from pathlib import Path
from typing import Any


def load_inputs(filepath: Path) -> defaultdict[int, list[list]]:
    data = defaultdict(list)
    for line in filepath.read_text().splitlines():
        result, inputs = line.split(":")
        data[int(result)].append([int(v) for v in inputs.strip().split(" ")])
    return data


def gen_combinations(elements: Any, size: int):
    return product(elements, repeat=size)


def add(a, b):
    return a + b


def mul(a, b):
    return a * b


def concat(a, b):
    return int(str(a) + str(b))


def eval_test_data(test_inputs: defaultdict[int, list[list]], operators: list[callable]) -> int:
    total_sum = 0
    for result, test_inputs in test_inputs.items():
        for test_input in test_inputs:
            combinations = gen_combinations(operators, len(test_input) - 1)
            for combination in combinations:
                eval_result = test_input[0]
                for i, func in enumerate(combination):
                    eval_result = func(eval_result, test_input[i + 1])
                if eval_result == result:
                    total_sum += eval_result
                    break
    return total_sum


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"
    data = load_inputs(input_path)

    operators = [add, mul]
    print("FIRST PART", eval_test_data(data, operators))
    operators.append(concat)
    print("SECOND PART", eval_test_data(data, operators))
