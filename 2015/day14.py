import sys
from pathlib import Path


def part_one(raindeer_data: list[tuple[int, int, int]]) -> int:
    total_secs = 2503
    distances = []
    for speed, fly_time, rest_time in raindeer_data:
        distance_per_fly_time = speed * fly_time
        full_cycles = total_secs // (fly_time + rest_time)
        distance_full_cycles = full_cycles * distance_per_fly_time
        time_delta = total_secs % (fly_time + rest_time)
        rest_of_fly_time = time_delta if time_delta < fly_time else fly_time
        total_distance = distance_full_cycles + rest_of_fly_time * speed
        distances.append(total_distance)
    return max(distances)


def part_two(raindeer_data: list[tuple[int, int, int]]) -> int:
    distances = [0 for _ in range(len(raindeer_data))]
    scores = [0 for _ in range(len(raindeer_data))]
    for s in range(2503):
        for i, (speed, fly_time, rest_time) in enumerate(raindeer_data):
            distances[i] += speed if s % (fly_time + rest_time) < fly_time else 0
        max_d = max(distances)
        for i, d in enumerate(distances):
            if d == max_d:
                scores[i] += 1
    return max(scores)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"
    data = input_path.read_text().strip()

    raindeer_data = []
    for line in data.splitlines():
        splitted = line.split()
        speed = int(splitted[3])
        fly_time = int(splitted[6])
        rest_time = int(splitted[-2])
        raindeer_data.append((speed, fly_time, rest_time))

    print("FIRST PART", part_one(raindeer_data))
    print("SECOND PART", part_two(raindeer_data))
