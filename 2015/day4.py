from hashlib import md5


def hash_starts_with_n_zeros(n: int):
    i = 0
    s = "0"*n
    while not md5((data + str(i)).encode()).hexdigest().startswith(s):
        i+=1
    return i

def part_one(data: str) -> int:
    return hash_starts_with_n_zeros(5)

def part_two(data: str) -> int:
    return hash_starts_with_n_zeros(6)


if __name__ == "__main__":
    data = "xyz"

    print("FIRST PART", part_one(data))
    print("SECOND PART", part_two(data))
