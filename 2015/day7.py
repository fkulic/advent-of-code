from collections import defaultdict, deque
from copy import deepcopy
from dataclasses import dataclass
import sys
from pathlib import Path


@dataclass(frozen=True)
class Op:
    op: str | None
    n1_in: str
    n2_in: str | None = None

    def can_execute(self, values: dict) -> bool:
        n1 = int(self.n1_in) if self.n1_in.isnumeric() else values.get(self.n1_in)
        if self.n2_in is not None:
            n2 = int(self.n2_in) if self.n2_in.isnumeric() else values.get(self.n2_in)
            return n1 is not None and n2 is not None
        return n1 is not None

    def execute(self, values: dict) -> int:
        n1 = int(self.n1_in) if self.n1_in.isnumeric() else values.get(self.n1_in)
        if self.n2_in:
            n2 = int(self.n2_in) if self.n2_in.isnumeric() else values.get(self.n2_in)

        match self.op:
            case None:
                ret = n1
            case "AND":
                ret = n1 & n2
            case "OR":
                ret = n1 | n2
            case "LSHIFT":
                ret = n1 << n2
            case "RSHIFT":
                ret = n1 >> n2
            case "NOT":
                ret = 256 * 256 + (~n1)
        return ret & 65535


def run_wires_get_a(operations: dict[str, Op], values: dict[str, int]) -> int:
    do = deque(set(operations.keys() - set(values.keys())))
    while do:
        n_out = do.popleft()
        op = operations[n_out]
        if op.can_execute(values):
            values[n_out] = op.execute(values)
        else:
            do.append(n_out)
    return values["a"]


def part_one(operations: dict[str, Op], values: dict[str, int]) -> int:
    return run_wires_get_a(deepcopy(operations), deepcopy(values))


def part_two(operations: dict[str, Op], values: dict[str, int]) -> int:
    a = part_one(operations, values)
    values = deepcopy(values)
    values["b"] = a
    return run_wires_get_a(deepcopy(operations), values)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"
    lines = input_path.read_text().strip().splitlines()

    ops = defaultdict(list)
    values = {}

    G = {}
    for line in lines:
        left, node_out = line.split("->")
        left = left.strip().split()
        node_out = node_out.strip()
        match len(left):
            case 1:
                # Assignment
                if left[0].isnumeric():
                    values[node_out] = int(left[0])
                else:
                    G[node_out] = Op(None, left[0])
            case 2:
                # Complement
                op, node_in = left
                G[node_out] = Op(op, node_in)
            case 3:
                o1, op, o2 = left
                G[node_out] = Op(op, o1, o2)

    print("FIRST PART", part_one(G, values))
    print("SECOND PART", part_two(G, values))
