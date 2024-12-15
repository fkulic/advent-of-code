def increment_str(a: str) -> str:
    for l in "iol":
        if (i := a.find(l)) != -1:
            return a[:i] + chr(ord(l) + 1) + "a" * (len(a) - i - 1)
    l_a = []
    for i, c in enumerate(a[::-1]):
        was_z = False
        if c == "z":
            l_a.append("a")
            was_z = True
        else:
            l_a.append(chr(ord(c) + 1))
        if not was_z:
            return a[: len(a) - i - 1] + "".join(reversed(l_a))
    return ""


def is_valid(a: str) -> bool:
    pairs = set()
    i = 1
    three_increasing = False
    while i < len(a):
        if a[i - 1] == a[i]:
            pairs.add(a[i])
        if not three_increasing and i < len(a) - 2:
            nums = [ord(c) for c in a[i - 1 : i + 2]]
            if nums[2] - nums[1] == 1 and nums[1] - nums[0] == 1:
                three_increasing = True
        i += 1
    return len(pairs) > 1 and three_increasing and "i" not in a and "o" not in a and "l" not in a


def find_next_valid_pw(pw: str) -> str:
    pw = increment_str(pw)
    while not is_valid(pw):
        pw = increment_str(pw)
    return pw


if __name__ == "__main__":
    p1 = find_next_valid_pw("invalidpw")
    print("FIRST PART", p1)
    print("SECOND PART", find_next_valid_pw(p1))
