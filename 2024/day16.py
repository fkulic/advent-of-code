import sys
from collections import deque
from dataclasses import dataclass
from pathlib import Path


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


class Node:
    def __init__(self, position: Point, direction: Point, parent=None) -> None:
        self.position: Point = position
        self.direction: Point = direction
        self.parent: "Node" = parent
        self.cost: int = 0
        if parent is not None:
            cost = 1 if parent.direction == direction else 1001
            self.cost += parent.cost + cost

    def __eq__(self, other) -> bool:
        return self.position == other.position

    def __repr__(self) -> str:
        parent = f"p:{self.parent.position}, d{self.parent.direction}" if self.parent else "None"
        return f"Node: p:{self.position}, d:{self.direction}, cost:{self.cost} par:{parent}"


def get_directions(current_direction: Point) -> list[Point]:
    if current_direction.x != 0:
        return [current_direction, Point(0, -1), Point(0, 1)]
    else:
        return [current_direction, Point(1, 0), Point(-1, 0)]


def count_best_seats(end_nodes: list[Node]) -> int:
    c = set([E])
    for end_node in end_nodes:
        n = end_node
        while (n := n.parent) is not None:
            c.add(n.position)
    return len(c)


def both_parts() -> tuple[int, int]:
    start_node = Node(S, Point(0, 1))
    Q = deque([start_node])
    end_nodes = []
    visited_cost = {}
    while Q:
        node = Q.popleft()
        next_pds = [(p, d) for d in get_directions(node.direction) if (p := node.position + d) not in WALLS]

        for next_p, next_d in next_pds:
            next_node = Node(next_p, next_d, node)
            if next_p in visited_cost and (visited_cost[next_p] + 1000) < next_node.cost:
                continue
            visited_cost[next_p] = next_node.cost

            if next_p == E:
                if len(end_nodes) > 0:
                    if next_node.cost > end_nodes[0].cost:
                        continue
                end_nodes.append(next_node)
            else:
                Q.append(next_node)

    lowest_score = min(end_nodes, key=lambda x: x.cost).cost
    end_nodes = [n for n in end_nodes if n.cost == lowest_score]
    second_part = count_best_seats(end_nodes)
    return lowest_score, second_part


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    data = [list(line) for line in input_path.read_text().strip().splitlines()]

    invalid_point = Point(-1, -1)
    S, E = invalid_point, invalid_point
    DIMENSIONS: Point = invalid_point
    WALLS: set[Point] = set()
    for i, line in enumerate(data):
        for j, c in enumerate(line):
            if c == "#":
                WALLS.add(Point(i, j))
            elif c == "S":
                S = Point(i, j)
            elif c == "E":
                E = Point(i, j)

    first, second = both_parts()
    print("FIRST PART", first)
    print("SECOND PART", second)
