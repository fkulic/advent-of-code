import sys
from collections import deque
from pathlib import Path


def part_one(input: list[int]):
    id = 0
    spaces = set()
    files = deque()
    total_count = 0
    for i, c in enumerate(input):
        if i % 2:
            spaces.update(range(total_count, total_count + c))
        else:
            files.extend([id] * c)
            id += 1
        total_count += c

    compressed_order = []
    for i in range(total_count):
        if i in spaces:
            compressed_order.append(files.pop())
        else:
            compressed_order.append(files.popleft())

        if not files:
            break

    return sum(i * x for i, x in enumerate(compressed_order))


def print_order(files, size):
    a = ["."] * size
    for f_idx, f_size, id in files:
        for i in range(f_idx, f_idx + f_size):
            a[i] = str(id)
    print("".join(a))


def part_two(input: list[int]):
    id = 0
    files = []
    spaces = []
    total_count = 0
    for i, c in enumerate(input):
        if i % 2:
            spaces.append((total_count, c))
        else:
            files.append((total_count, c, id))
            id += 1
        total_count += c

    for i, (f_idx, f_size, id) in reversed(list(enumerate(files))):
        # print_order(files, total_count)
        s_idx, s_size = None, None
        for i_in_spaces, (j, s) in enumerate(spaces):
            if j > f_idx:
                break
            if f_size <= s:
                s_idx, s_size = j, s
                break

        if s_idx:
            spaces.pop(i_in_spaces)
            spaces.append((f_idx, f_size))
            if f_size == s_size:
                files[i] = s_idx, s_size, id
            else:
                diff = s_size - f_size
                files[i] = s_idx, f_size, id
                spaces.append((s_idx + f_size, diff))
            spaces = sorted(spaces, key=lambda x: x[0])

    return sum(id * sum(range(f_idx, f_idx + f_size)) for f_idx, f_size, id in files)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"
    input = [int(x) for x in Path(input_path).read_text().strip()]

    print("PART_ONE", part_one(input))
    print("PART TWO", part_two(input))
