import sys
from pathlib import Path


def ishex(s: str) -> bool:
    try:
        int(s, 16)
        return True
    except ValueError:
        return False


def part_one(data: list[str]) -> int:
    str_len = []
    mem_len = []
    for line in data:
        str_len.append(len(line))
        remove_escaped = line[1:-1].replace(r"\"", '"').replace(r"\\", "\\")
        i = 0
        while (i := remove_escaped.find(r"\x", i)) != -1:
            if i + 3 >= len(remove_escaped) or not ishex(remove_escaped[i + 2 : i + 4]):
                i += 1
            else:
                remove_escaped = remove_escaped.replace(remove_escaped[i : i + 4], "a")
        mem_len.append(len(remove_escaped))
    return sum(str_len) - sum(mem_len)


def part_two(data: list[str]) -> int:
    str_len = []
    escaped_len = []
    for line in data:
        str_len.append(len(line))
        escaped = line.replace("\\", r"\\").replace(r'"', r"\"")
        escaped_len.append(len(escaped) + 2)
    return sum(escaped_len) - sum(str_len)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"
    data = input_path.read_text().strip().splitlines()

    print("FIRST PART", part_one(data))
    print("SECOND PART", part_two(data))
