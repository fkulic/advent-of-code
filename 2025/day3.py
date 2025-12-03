import sys
from pathlib import Path


def part_one(banks: list[list[int]]) -> int:
    total_joltage = 0
    for bank in banks:
        max_not_last = max(bank[:-1])
        max_i = bank.index(max_not_last)
        max_after_i = max(bank[max_i + 1 :])
        total_joltage += max_not_last * 10 + max_after_i
    return total_joltage


def get_biggest_bank(leftover: str, current_bank: str = "") -> int:
    if len(current_bank) == 12:
        return int(current_bank)

    current_len = len(current_bank)
    needed = 11 - current_len
    leftover_len = len(leftover)
    sub_bank = leftover[: leftover_len - needed]
    max_has_room = max(sub_bank)
    max_indices = [i for i, e in enumerate(sub_bank) if e == max_has_room]
    for i in max_indices:
        return get_biggest_bank(leftover[i + 1 :], current_bank + max_has_room)


def part_two(banks: list[str]) -> int:
    return sum(get_biggest_bank(bank) for bank in banks)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    if not input_path.is_file():
        print(f"{input_path} is not a file")
        sys.exit(1)

    banks = input_path.read_text().strip().splitlines()
    int_banks = [[int(c) for c in line] for line in banks]

    print("FIRST PART", part_one(int_banks))
    print("SECOND PART", part_two(banks))
