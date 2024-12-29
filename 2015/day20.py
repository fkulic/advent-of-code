from collections import defaultdict
import math
import sys


def get_divisors(n) -> set[int]:
    divisors = set([1])
    for i in range(1, math.isqrt(n) + 1):
        if n % i == 0:
            divisors.add(i)
            if i != n // i:
                divisors.add(n // i)
    return divisors


def part_one(target: int) -> int:
    for n in range(1, target):
        presents = sum(d * 10 for d in get_divisors(n))
        if presents >= target:
            return n
    raise Exception("Didn't find the first house")


def part_two(target: int) -> int:
    done = defaultdict(int)
    for n in range(1, target):
        presents = 0
        for d in get_divisors(n):
            if done[d] < 50:
                presents += d * 11
            done[d] += 1
        if presents >= target:
            return n
    raise Exception("Didn't find the first house")


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No target number"
    assert sys.argv[1].isdecimal()

    target = int(sys.argv[1])

    print("FIRST PART", part_one(target))
    print("SECOND PART", part_two(target))
