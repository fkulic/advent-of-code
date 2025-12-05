import sys
from pathlib import Path


def part_one(ranges, ingredients) -> int:
    good_ingredients = set()
    for start, end in ranges:
        for i in ingredients:
            if start <= i <= end:
                good_ingredients.add(i)
    return len(good_ingredients)


def part_two(ranges) -> int:
    ranges = sorted(ranges, key=lambda x: x[0])
    remove_indices = set()
    for i in range(1, len(ranges)):
        p_s, p_e = ranges[i - 1]
        c_s, c_e = ranges[i]
        if p_e >= c_s:
            remove_indices.add(i - 1)
            ranges[i][0] = min(p_s, c_s)
            ranges[i][1] = max(p_e, c_e)

    return sum(
        end - start + 1
        for i, (start, end) in enumerate(ranges)
        if i not in remove_indices
    )


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    if not input_path.is_file():
        print(f"{input_path} is not a file")
        sys.exit(1)

    ranges_data, ingredients_data = input_path.read_text().strip().split("\n\n")

    ranges = []
    for row in ranges_data.splitlines():
        ranges.append([int(x) for x in row.split("-")])

    ingredients = set()
    for row in ingredients_data.strip().splitlines():
        ingredients.add(int(row.strip()))

    print("FIRST PART", part_one(ranges, ingredients))
    print("SECOND PART", part_two(ranges))
