import sys
from pathlib import Path


def find_all_occurrences(string: str, substring: str) -> list[int]:
    indices = []
    start = 0
    while True:
        index = string.find(substring, start)
        if index == -1:
            break
        indices.append(index)
        start = index + 1
    return indices


def replace_substring_at_index(string: str, index: int, old: str, new: str) -> str:
    if string[index : index + len(old)] != old:
        raise ValueError("The substring at the specified index does not match the old substring.")
    return string[:index] + new + string[index + len(old) :]


def part_one(transformations: list[tuple[str, str]], starting_molecule: str) -> int:
    new_molecules = set()
    for t_from, t_to in transformations:
        indices = find_all_occurrences(starting_molecule, t_from)
        for i in indices:
            new_molecules.add(replace_substring_at_index(starting_molecule, i, t_from, t_to))
    return len(new_molecules)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"

    input_path = Path(sys.argv[1])
    assert input_path.is_file(), "Not file"

    transformations, starting = input_path.read_text().strip().split("\n\n")
    transformations = [(s[0], s[1]) for line in transformations.splitlines() for s in [line.split(" => ")]]

    print("FIRST PART", part_one(transformations, starting))
    # print("SECOND PART", second)
