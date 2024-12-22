import sys
from collections import defaultdict
from pathlib import Path


def get_next_price(n: int) -> int:
    n ^= n * 64
    n %= 16777216
    n ^= n // 32
    n %= 16777216
    n ^= n * 2048
    n %= 16777216
    return n


def get_2000th_price(n: int):
    for _ in range(2000):
        n = get_next_price(n)
    return n


def part_one(data: list[int]) -> int:
    return sum(get_2000th_price(x) for x in data)


def part_two(data: list[int]) -> int:
    prices = defaultdict(list)
    for i, next_price in enumerate(data):
        last_4_diffs = []
        last_digit = 0
        for j in range(2000):
            previous_last_digit = last_digit
            next_price = get_next_price(next_price)
            last_digit = next_price % 10
            if j != 0:
                last_4_diffs.append(last_digit - previous_last_digit)
            if len(last_4_diffs) > 4:
                last_4_diffs = last_4_diffs[1:]
            if len(last_4_diffs) > 3:
                prices[*last_4_diffs].append((i, last_digit))

    total_prices = []
    for _, values in prices.items():
        seen = set()
        total_bananas = 0
        for i, digit in values:
            if i in seen:
                continue
            seen.add(i)
            total_bananas += digit
        total_prices.append(total_bananas)
    return max(total_prices)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"
    data = [int(x) for x in input_path.read_text().strip().splitlines()]

    print("FIRST PART", part_one(data))
    print("SECOND PART", part_two(data))
