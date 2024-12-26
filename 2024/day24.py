from collections import deque
from copy import deepcopy
import random
import re
import sys
from pathlib import Path


def execute(values: dict[str, int], operations: dict[str, tuple[str, str, str]]) -> None:
    executed = set()
    while len(executed) != len(operations):
        for k in set(operations.keys()) - executed:
            in1, in2, op = operations[k]
            if k not in executed and in1 in values and in2 in values:
                executed.add(k)
                in1 = values[in1]
                in2 = values[in2]
                r = None
                match op:
                    case "AND":
                        r = in1 & in2
                    case "OR":
                        r = in1 | in2
                    case "XOR":
                        r = in1 ^ in2
                assert r is not None
                values[k] = r


def part_one(values: dict[str, int], operations: dict[str, tuple[str, str, str]]) -> int:
    execute(values, operations)
    out = 0
    for k, v in values.items():
        if k.startswith("z"):
            out += v << int(k.split("z")[-1])
    return out


class OpNode:
    def __init__(self, name, in1=None, in2=None, operation=None):
        self.name = name
        match = re.match(r"(\S)(\d\d)", name)
        self.group = match.group(0) if match else None
        self.bit = match.group(1) if match else None
        self.in1 = in1
        self.in2 = in2
        self.operation = operation

    def __repr__(self) -> str:
        operators = f"[{self.in1}] [{self.in2}]" if self.in1 else ""
        op = f"{self.in1.name} {self.operation} {self.in2.name}" if self.operation is not None else ""
        return f"{self.name}: {op} {operators}"


def check_validity(values: dict[str, int], operations: dict[str, tuple[str, str, str]]) -> bool:
    vs = deepcopy(values)
    execute(vs, operations)
    x, y, z = 0, 0, 0
    for k, v in vs.items():
        if k.startswith("x"):
            x += v << int(k.split("x")[-1])
        elif k.startswith("y"):
            y += v << int(k.split("y")[-1])
        elif k.startswith("z"):
            z += v << int(k.split("z")[-1])
    if x + y == z:
        return True

    actual = bin(x + y).removeprefix("0b")
    binz = bin(z).removeprefix("0b")
    for i in range(len(actual) - 1, 0, -1):
        if actual[i] != binz[i]:
            print(f"diff at bit {len(actual)-1-i}")

    print(" 44444443333333333222222222211111111110000000000")
    print(" 65432109876543210987654321098765432109876543210")
    print(f" {bin(x)}")
    print(f" {bin(y)}")
    print(bin(z))
    print(f"{bin(x+y)} actual x+y")
    return False


def out_dot(operations: dict[str, tuple[str, str, str]]):
    out_path = Path(__file__).parent / "day24_graph.dot"
    colors = {"AND": '"blue"', "OR": '"red"', "XOR": '"green"'}
    with out_path.open("w") as f:
        f.write("digraph {\n")
        for node_out, (in1, in2, op) in operations.items():
            color = colors[op]
            f.write(f"{node_out} [color={color}]\n")
            f.write(f"{in1} -> {node_out}\n")
            f.write(f"{in2} -> {node_out}\n")
        f.write("}")


def swap(node_names: list[tuple[str, str]], operations: dict[str, tuple[str, str, str]]) -> None:
    for n1, n2 in node_names:
        operations[n1], operations[n2] = operations[n2], operations[n1]


def part_two(values: dict[str, int], operations: dict[str, tuple[str, str, str]]):
    # First three can be found easiely by looking at graphviz output colors and hint you get from check_validity function
    # Last error is hard to spot and occurs only for some inputs, so randomize input until check_validity fails to get hint for a bit
    swaps = []
    swap(swaps, operations)

    for _ in range(1000):
        if not (check_validity(values, operations)):
            break
        for k in values:
            values[k] = random.choice([0, 1])

    out_dot(operations)

    # "Manual solution, might try to find algorithm later"
    return ",".join(sorted([x for swap in swaps for x in swap]))

    # Not used really
    z_outs = []
    for out in operations:
        if out.startswith("z"):
            z_outs.append(out)
    z_outs.sort()

    nodes = {}
    z_nodes = []
    visited = set()
    for z in z_outs:

        Q = deque([z])
        while Q:
            o = Q.popleft()
            in1, in2, op = operations[o]

            if o in visited:
                continue

            if in1 in nodes:
                in1_node = nodes[in1]
            else:
                in1_node = OpNode(in1)
                nodes[in1] = in1_node

            if in2 in nodes:
                in2_node = nodes[in2]
            else:
                in2_node = OpNode(in2)
                nodes[in2] = in2_node

            if o in nodes:
                o_node = nodes[o]
                o_node.in1 = in1_node
                o_node.in2 = in2_node
                o_node.operation = op
            else:
                o_node = OpNode(o, in1_node, in2_node, op)
                nodes[o] = o_node

            if o.startswith("z"):
                z_nodes.append(o_node)

            if in1 in operations:
                Q.append(in1)
            if in2 in operations:
                Q.append(in2)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"

    initial_values, operation_lines = input_path.read_text().strip().split("\n\n")

    values = {}
    for iv_line in initial_values.splitlines():
        k, v = iv_line.split(": ")
        values[k] = int(v)

    operations = {}
    for op_line in operation_lines.splitlines():
        in1, op, in2, _, out = op_line.split(" ")
        operations[out] = (in1, in2, op)

    print("FIRST PART", part_one(deepcopy(values), deepcopy(operations)))
    print("SECOND PART", part_two(values, operations))
