from hashlib import md5


def hash_starts_with_n_zeros(data: str, n: int) -> int:
    i = 0
    s = "0" * n
    while not md5((data + str(i)).encode()).hexdigest().startswith(s):
        i += 1
    return i


if __name__ == "__main__":
    data = "xyz"

    print("FIRST PART", hash_starts_with_n_zeros(data, 5))
    print("SECOND PART", hash_starts_with_n_zeros(data, 6))
