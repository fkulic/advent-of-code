from functools import cache


@cache
def look_and_say(a: str) -> str:
    c = a[0]
    count = 1
    new_a = []
    for current_c in a[1:]:
        if current_c == c:
            count += 1
        else:
            new_a.append(str(count))
            new_a.append(c)
            c = current_c
            count = 1
    new_a.append(str(count))
    new_a.append(a[-1])
    return "".join(new_a)


def part_one(a: int) -> int:
    str_a = str(a)
    for _ in range(40):
        str_a = look_and_say(str_a)
    return len(str_a)


def part_two(a: int) -> int:
    str_a = str(a)
    for _ in range(50):
        str_a = look_and_say(str_a)
    return len(str_a)


if __name__ == "__main__":
    print("FIRST PART", part_one(1))
    print("SECOND PART", part_two(1))
