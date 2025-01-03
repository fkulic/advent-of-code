import sys
from pathlib import Path

TALL, WIDE = 6, 25


def part_one(encoded_image: list[list[list[int]]]) -> int:
    zero_digits = [sum(1 for line in layer for d in line if d == 0) for layer in encoded_image]
    min_zeros = min(zero_digits)
    layer = zero_digits.index(min_zeros)
    ones = sum(1 for line in encoded_image[layer] for d in line if d == 1)
    return (TALL * WIDE - ones - min_zeros) * ones


def part_two(encoded_image: list[list[list[int]]]) -> str:
    decoded_image = ["\n"]
    for x in range(TALL):
        decoded_line = []
        for y in range(WIDE):
            for i in range(len(encoded_image)):
                match encoded_image[i][x][y]:
                    case 0:
                        decoded_line.append(" ")
                        break
                    case 1:
                        decoded_line.append("\u25a0")
                        break
        decoded_image.append("".join(decoded_line))
    return "\n".join(decoded_image)

if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"

    encoded_image = []
    x, y = 0, 0
    for i, c in enumerate(input_path.read_text().strip()):
        x = (i // WIDE) % TALL
        y = i % WIDE
        if x == 0 and y == 0:
            encoded_image.append([])
        if y == 0:
            encoded_image[-1].append([])
        encoded_image[-1][-1].append(int(c))

    print("FIRST PART", part_one(encoded_image))
    print("SECOND PART", part_two(encoded_image))
