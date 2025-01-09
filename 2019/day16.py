import sys
from pathlib import Path


def get_pattern(n, pattern_len) -> list[int]:
    pattern = []
    while len(pattern) < pattern_len + 1:
        for x in [0, 1, 0, -1]:
            pattern.extend([x] * n)
    return pattern[1 : pattern_len + 1]


def fft(signal: list[int]) -> list[int]:
    out = []
    digit = 1
    while len(out) != len(signal):
        pattern = get_pattern(digit, len(signal))
        x = 0
        for i, c in enumerate(signal):
            x += pattern[i] * c
        out.append(abs(x) % 10)
        digit += 1
    return out


def part_one(signal: list[int]) -> str:
    for _ in range(100):
        signal = fft(signal)
    return "".join(str(x) for x in signal[:8])


def analyze_pattern(signal, start=None, count=8) -> None:
    start = start or len(signal) - 10
    for n in range(start - 1, start - count, -1):
        x = 1
        pattern = get_pattern(n, len(signal))
        for i, p in enumerate(pattern):
            if i == 0:
                continue
            last = pattern[i - 1]
            if p == last:
                x += 1
            else:
                print(f"{last} occurs {x} times", end=", ")
                x = 1
        print(f"{pattern[-1]} occurs {x} times")


def part_two(signal: list[int], start_from: int) -> str:
    signal = signal * 10000

    # analyze_pattern(signal)
    # analyze_pattern(signal, start_from+9)

    signal = signal[start_from:]
    signal.reverse()

    for _ in range(100):
        new_signal = []
        new_digit = 0
        for x in signal:
            new_digit = (x + new_digit) % 10
            new_signal.append(new_digit)
        signal = new_signal

    return "".join(map(str, signal[-8:][::-1]))


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"
    data = input_path.read_text().strip()

    signal = [int(x) for x in data]
    digit_from = int(data[:7])

    print("FIRST PART", part_one(signal))
    print("SECOND PART", part_two(signal, digit_from))
