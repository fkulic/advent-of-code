import sys
from collections import deque
from functools import cache
from pathlib import Path


def part_one(server_connections, start_node) -> int:
    if start_node not in server_connections:
        return 0

    paths = 0
    stack = deque([start_node])
    while stack:
        for o in server_connections.get(stack.popleft(), []):
            if o == "out":
                paths += 1
            else:
                stack.append(o)
    return paths


class PathCounter:
    def __init__(self, connections: dict[str, set[str]], must_visit: list[str]):
        self._connections = connections
        self._expected_visits = 0
        self._must_visit = {}
        for i, node in enumerate(must_visit):
            x = 1 << i
            self._must_visit[node] = x
            self._expected_visits += x

    @cache
    def paths_to_out(self, node, visited=0):
        visited |= self._must_visit.get(node, 0)

        if node == "out":
            return int(visited == self._expected_visits)

        return sum(self.paths_to_out(c, visited) for c in self._connections[node])


def part_two(server_connections, start_node) -> int:
    c = PathCounter(server_connections, ["fft", "dac"])
    return c.paths_to_out(start_node)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    if not input_path.is_file():
        print(f"{input_path} is not a file")
        sys.exit(1)

    server_connections = {}
    for line in input_path.read_text().strip().splitlines():
        name, outs = line.split(": ")
        server_connections[name] = outs.strip().split()

    print("FIRST PART", part_one(server_connections, "you"))
    print("SECOND PART", part_two(server_connections, "svr"))
