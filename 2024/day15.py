import sys
from collections import deque
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other) -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, a: int) -> "Point":
        return Point(self.x * a, self.y * a)


class Directions:
    _DIRECTIONS = [Point(-1, 0), Point(0, 1), Point(1, 0), Point(0, -1)]

    def __init__(self, moves: str) -> None:
        self.moves = moves
        self._i = 0

    def reset(self) -> None:
        self._i = 0

    @classmethod
    def get_direction(cls, a: str) -> Point:
        assert a in "^>v<"
        match a:
            case "^":
                return cls._DIRECTIONS[0]
            case ">":
                return cls._DIRECTIONS[1]
            case "v":
                return cls._DIRECTIONS[2]
            case "<":
                return cls._DIRECTIONS[3]

    def next(self) -> Point | None:
        if self._i == len(self.moves):
            return None
        direction = self.get_direction(self.moves[self._i])
        self._i += 1
        return direction


def first_part(warehouse: list[list[str]], directions: Directions) -> int:
    robot = None
    boxes = set()
    walls = set()
    for i, r in enumerate(warehouse):
        for j, c in enumerate(r):
            match c:
                case "@":
                    robot = Point(i, j)
                case "O":
                    boxes.add(Point(i, j))
                case "#":
                    walls.add(Point(i, j))
    assert robot
    while d := directions.next():
        in_front = robot + d
        if in_front in walls:
            continue
        if in_front in boxes:
            check = deque([in_front])
            b_to_move = 0
            while check:
                b = check.popleft()
                b_in_front = b + d
                if b_in_front in walls:
                    b_to_move = 0
                    break
                if b_in_front in boxes:
                    b_to_move += 1
                    check.append(b_in_front)
                else:
                    b_to_move += 1
                    break
            if b_to_move:
                robot = in_front
                boxes.remove(in_front)
                boxes.add(in_front + d * b_to_move)
        else:
            robot = in_front
    return sum(p.x * 100 + p.y for p in boxes)


class P2Solution:

    def __init__(self, warehouse: list[list[str]], directions: Directions) -> None:
        self.directions: Directions = directions
        self.boxes_p: dict[Point, int] = dict()
        self.boxes: list[tuple[Point, Point]] = []
        self.walls: set[Point] = set()
        self.dimensions = Point(len(warehouse), len(warehouse[0] * 2))
        for i, r in enumerate(warehouse):
            for j, c in enumerate(r):
                p1 = Point(i, 2 * j)
                p2 = Point(i, 2 * j + 1)
                match c:
                    case "@":
                        self.robot: Point = p1
                    case "O":
                        self.boxes_p[p1] = self.boxes_p[p2] = len(self.boxes)
                        self.boxes.append((p1, p2))
                    case "#":
                        self.walls.update((p1, p2))

    def solve(self) -> int:
        while d := directions.next():
            in_front = self.robot + d
            if in_front in self.walls:
                continue

            if in_front not in self.boxes_p:
                self.robot = in_front
            elif d.x != 0:
                self._move_vertically(in_front, d)
            else:
                self._move_horizontally(in_front, d)

        return sum(p.x * 100 + p.y for p, _ in self.boxes)

    def _move_vertically(self, in_front: Point, direction: Point):
        idx: int = self.boxes_p[in_front]
        check: deque[tuple[Point, Point]] = deque([self.boxes[idx]])
        visited = set()
        b_to_move = set()

        while check:
            box = check.popleft()
            for p in box:
                if p in visited:
                    continue
                visited.add(p)
                b_in_front = p + direction
                if b_in_front in self.walls:
                    return
                b_to_move.add(self.boxes_p[p])
                if b_in_front in self.boxes_p:
                    check.append(self.boxes[self.boxes_p[b_in_front]])

        self.robot = in_front
        self._move_boxes(b_to_move, direction)

    def _move_horizontally(self, in_front: Point, direction: Point):
        b_to_move = set()
        idx = self.boxes_p[in_front]
        check = deque([self.boxes[idx]])
        while check:
            b1, b2 = check.popleft()
            p = b1 if direction.y == -1 else b2
            b_in_front = p + direction
            if b_in_front in self.walls:
                return
            b_to_move.add(self.boxes_p[p])
            if b_in_front in self.boxes_p:
                idx_in_front = self.boxes_p[b_in_front]
                check.append(self.boxes[idx_in_front])

        self.robot = in_front
        self._move_boxes(b_to_move, direction)

    def _move_boxes(self, b_to_move: set[int], direction: Point) -> None:
        temp_boxes = deepcopy(self.boxes)
        for idx in b_to_move:
            b1, b2 = temp_boxes[idx]
            b1_new, b2_new = b1 + direction, b2 + direction
            self.boxes[idx] = (b1_new, b2_new)
            del self.boxes_p[b1]
            del self.boxes_p[b2]
        for idx in b_to_move:
            (b1, b2) = self.boxes[idx]
            self.boxes_p[b1] = idx
            self.boxes_p[b2] = idx


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    warehouse, moves = input_path.read_text().strip().split("\n\n")
    warehouse = [list(line.strip()) for line in warehouse.splitlines()]
    directions = Directions("".join([m.strip() for m in moves]))

    print("FIRST PART", first_part(warehouse, directions))
    directions.reset()

    part_two = P2Solution(warehouse, directions)
    print("SECOND PART", part_two.solve())
