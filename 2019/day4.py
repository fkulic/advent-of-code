import sys


def both_parts(start, end) -> tuple[int, int]:
    first, second = 0, 0
    for pw in range(start, end + 1):
        str_pw = str(pw)
        increase = True
        repeating = False
        has_double_repeat = False
        for i in range(1, len(str_pw)):
            if str_pw[i - 1] > str_pw[i]:
                increase = False
                break
            if str_pw[i - 1] == str_pw[i]:
                if str_pw[i] * 3 not in str_pw:
                    has_double_repeat = True
                repeating = True
        if increase:
            if repeating:
                first += 1
            if has_double_repeat:
                second += 1
    return first, second


if __name__ == "__main__":
    assert len(sys.argv) > 2, "no start range, end range arguments"
    assert sys.argv[1].isdigit(), "start arg not positive integer"
    assert sys.argv[2].isdigit(), "end arg not positive integer"

    first, second = both_parts(int(sys.argv[1]), int(sys.argv[2]))
    print("FIRST PART", first)
    print("SECOND PART", second)
