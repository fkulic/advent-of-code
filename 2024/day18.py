from collections import deque
from dataclasses import dataclass
import heapq
import re
import sys
from pathlib import Path


def ints_in_str(s: str) -> list[int]:
    return [int(x) for x in re.findall(r"(-?\d+)", s)]


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other) -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, a: int) -> "Point":
        return Point(self.x * a, self.y * a)

    def is_inside(self, dimensions: "Point") -> int:
        return 0 <= self.x < dimensions.x and 0 <= self.y < dimensions.y


class Node:
    def __init__(self, position: Point, parent=None) -> None:
        self.position: Point = position
        self.parent: "Node" = parent
        self.cost: int = 0
        if parent is not None:
            self.cost = self.parent.cost + 1

    def __lt__(self, other: "Node") -> bool:
        return self.cost < other.cost

    def __repr__(self) -> str:
        parent = f"p:{self.parent.position}" if self.parent else "None"
        return f"Node: p:{self.position}, cost:{self.cost} par:{parent}"


DIRECTIONS = [Point(-1, 0), Point(0, 1), Point(1, 0), Point(0, -1)]
DIMENSIONS_i = Point(71, 71)
DIMENSIONS_e = Point(7, 7)
N_i = 1024
N_e = 12


def print_map(taken: set[Point], node: Node):
    m = [["." for _ in range(DIMENSIONS.x)] for __ in range(DIMENSIONS.y)]
    for p in taken:
        m[p.x][p.y] = "#"
    m[node.position.x][node.position.y] = "O"
    while node := node.parent:
        m[node.position.x][node.position.y] = "X"
    for line in m:
        print("".join(line))
    print("\n\n")


def find_fastest_path(falling_bytes: list[Point], n) -> None | int:
    S = Point(0, 0)
    E = Point(DIMENSIONS.x - 1, DIMENSIONS.y - 1)
    taken = set(falling_bytes[:n])
    visited = {}
    S_node = Node(S)

    end_nodes = []

    Q = deque([S_node])
    while Q:
        node = Q.popleft()
        # print_map(taken, node)
        if node.position in visited and node.cost >= visited[node.position]:
            continue
        visited[node.position] = node.cost

        for d in DIRECTIONS:
            p_next = node.position + d
            if not p_next.is_inside(DIMENSIONS) or p_next in taken:
                continue
            else:
                new_node = Node(p_next, node)
                if p_next in visited and new_node.cost >= visited[p_next]:
                    continue
                if p_next == E:
                    heapq.heappush(end_nodes, new_node)
                else:
                    Q.append(new_node)

    if len(end_nodes) == 0:
        return None
    return heapq.heappop(end_nodes).cost


def part_one(falling_bytes: list[Point], n) -> int:
    fastest_path = find_fastest_path(falling_bytes, n)
    assert fastest_path is not None
    return fastest_path


def part_two(falling_bytes: list[Point]) -> str:
    for i in range(len(falling_bytes) - 1, 0, -1):
        path = find_fastest_path(falling_bytes, i)
        if path is not None:
            return f"{falling_bytes[i].x},{falling_bytes[i].y}"
    raise Exception("Not possible")


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    DIMENSIONS = DIMENSIONS_i if input_path.name == "18_input.txt" else DIMENSIONS_e
    N = N_i if input_path.name == "18_input.txt" else N_e

    falling_bytes = [Point(*ints_in_str(line)) for line in input_path.read_text().strip().splitlines()]

    print("FIRST PART", part_one(falling_bytes, N))
    print("SECOND PART", part_two(falling_bytes))
