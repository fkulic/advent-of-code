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
    def get_direction(cls, a: str) -> Point:  # type: ignore
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


def print_p1_warehouse(warehouse, walls, boxes, robot) -> None:
    for i in range(len(warehouse)):
        for j in range(len(warehouse[0])):
            p = Point(i, j)
            if p in walls:
                print("#", end="")
            elif p in boxes:
                print("O", end="")
            elif p == robot:
                print("@", end="")
            else:
                print(".", end="")
        print()


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
        # print_warehouse(warehouse, walls, boxes, robot)
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


def print_p2_warehouse(warehouse, walls, boxes, robot) -> None:
    for i in range(len(warehouse)):
        skip =set()
        for j in range(len(warehouse[0]) * 2):
            if j in skip:
                continue
            p = Point(i, j)
            if p in walls:
                print("#", end="")
            elif p in boxes:
                print("[]", end="")
                skip.add(j+1)
            elif p == robot:
                print("@", end="")
            else:
                print(".", end="")
        print()


def second_part(warehouse: list[list[str]], directions: Directions) -> int:
    robot = None
    boxes_p = dict()
    boxes = []
    walls = set()
    for i, r in enumerate(warehouse):
        for j, c in enumerate(r):
            p1 = Point(i, 2 * j)
            p2 = Point(i, 2 * j+1)
            match c:
                case "@":
                    robot = p1
                case "O":
                    boxes_p[p1] = len(boxes)
                    boxes_p[p2] = len(boxes)
                    boxes.append((p1, p2))
                case "#":
                    walls.add(p1)
                    walls.add(p2)
    assert robot
    while d := directions.next():
        # print_p2_warehouse(warehouse, walls, boxes_p, robot)
        in_front = robot + d
        vertical =  d.x != 0
        if in_front in walls:
            continue
        if in_front not in boxes_p:
            robot = in_front
        else:
            b_to_move = set()
            if vertical:
                idx = boxes_p[in_front]
                check = deque([])
                check.append([boxes[idx]])
                visited = set()
                while check:
                    can_move = True
                    for box in check.popleft():
                        for p in box:
                            if p in visited:
                                continue
                            visited.add(p)
                            b_in_front = p + d
                            if b_in_front in walls:
                                can_move = False
                                break
                            b_to_move.add(boxes_p[p])
                            if b_in_front in boxes_p:
                                idx_in_front = boxes_p[b_in_front]
                                check.append([boxes[idx_in_front]])
                    if not can_move:
                        b_to_move = set()
                        break
            else:
                idx = boxes_p[in_front]
                check = deque([boxes[idx]])
                while check:
                    b1, b2 = check.popleft()
                    p = b1 if d.y == -1 else b2
                    b_in_front = p + d
                    if b_in_front in walls:
                        b_to_move = set()
                        break
                    b_to_move.add(boxes_p[p])
                    if b_in_front in boxes_p:
                        idx_in_front = boxes_p[b_in_front]
                        check.append(boxes[idx_in_front])
                    else:
                        break

            if b_to_move:
                robot = in_front
            temp_boxes = deepcopy(boxes)
            for idx in b_to_move:
                b1, b2 = temp_boxes[idx]
                b1_new, b2_new = b1 + d, b2 + d
                boxes[idx] = (b1_new, b2_new)
                del boxes_p[b1]
                del boxes_p[b2]
            for idx in b_to_move:
                (b1, b2) = boxes[idx]
                boxes_p[b1] = idx
                boxes_p[b2] = idx

    # print_p2_warehouse(warehouse, walls, boxes_p, robot)
    return sum(p.x * 100 + p.y for p, _ in boxes)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    warehouse, moves = input_path.read_text().strip().split("\n\n")
    warehouse = [list(line.strip()) for line in warehouse.splitlines()]
    directions = Directions("".join([m.strip() for m in moves]))

    print("FIRST PART", first_part(warehouse, directions))
    directions.reset()
    print("SECOND PART", second_part(warehouse, directions))
