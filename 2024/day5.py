import sys
from collections import defaultdict
from pathlib import Path

Rules = defaultdict[int, set]

class InputData:
    before: Rules = defaultdict(set)
    after: Rules = defaultdict(set)
    manuals: list[list[int]] = []


def load_inputs(filepath: Path) -> InputData:
    data = InputData()
    for line in filepath.read_text().splitlines():
        line = line.strip()
        if "|" in line:
            x, y = line.split("|")
            data.before[int(x)].add(int(y))
            data.after[int(y)].add(int(x))
        elif "," in line:
            data.manuals.append([int(page) for page in line.split(",")])

    return data


def check_manual(must_be_before: Rules, manual: list[int]):
    for i, page in enumerate(manual[:-1]):
        for j in range(i + 1, len(manual)):
            following_page = manual[j]
            if following_page not in must_be_before[page]:
                return False
    return True


def get_ordered_manual(before: Rules, after: Rules, manual: list[int]) -> list[int]:
    ordered_manual = []
    manual_set = set(manual)
    weights = {page: len(after[page] & manual_set) for page in manual}
    lowest = [page for page, w in weights.items() if w == 0]
    while lowest:
        x = lowest.pop()
        ordered_manual.append(x)
        for after_x in before[x] & manual_set:
            weights[after_x] -= 1
            if weights[after_x] == 0:
                lowest.append(after_x)

    return ordered_manual


def both_parts(data: InputData) -> int:
    sum = 0
    sum_reordered = 0
    for manual in data.manuals:
        if check_manual(data.before, manual):
            sum += manual[len(manual) // 2]
        else:
            ordered_manual = get_ordered_manual(data.before, data.after, manual)
            sum_reordered += ordered_manual[len(ordered_manual) // 2]

    print("PART ONE SUM: ", sum)
    print("PART TWO SUM: ", sum_reordered)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"
    both_parts(load_inputs(input_path))
