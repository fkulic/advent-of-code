from functools import cache
import sys
from pathlib import Path

@cache
def divisors(n: int) -> list[int]:
    divisors = []
    for i in range(1, n // 2 +1 ):
        if n % i == 0:
            divisors.append(i)
    return divisors

def part_one(ranges: list[str]) -> int:
    total_sum = 0
    for r in ranges:
        start, end = r.split("-")
        for id in range(int(start), int(end)+1):
            str_id = str(id)
            half_len = len(str_id) // 2
            half_1, half_2 = str_id[half_len:], str_id[:half_len]
            if half_1 == half_2:
                total_sum += id
    return total_sum


def part_two(ranges: list[str]) -> int:
    total_sum = 0
    for r in ranges:
        start, end = r.split("-")
        for id in range(int(start), int(end)+1):
            str_id = str(id)
            for div in divisors(len(str_id)):
                parts = [str_id[i:i+div] for i in range(0, len(str_id), div)]
                good = True
                for i in range(1, len(parts)):
                    if parts[0] != parts[i]:
                        good = False
                        break
                if good:
                    total_sum += id
                    break
    return total_sum


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    if not input_path.is_file():
        print(f"{input_path} is not a file")
        sys.exit(1)

    data = input_path.read_text()
    ranges = [r.strip() for r in data.split(",")]

    print("FIRST PART", part_one(ranges))
    print("SECOND PART", part_two(ranges))
