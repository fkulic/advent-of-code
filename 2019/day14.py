import sys
from collections import defaultdict
from copy import deepcopy
from math import ceil
from pathlib import Path


def calculate_ore(reactions, out_quantity, out_name="FUEL", leftovers=defaultdict(int)):
    if out_name == "ORE":
        return out_quantity

    if leftovers[out_name] >= out_quantity:
        leftovers[out_name] -= out_quantity
        return 0

    out_quantity -= leftovers[out_name]
    leftovers[out_name] = 0

    produced_amount, chemicals_needed = reactions[out_name]
    times_to_run = ceil(out_quantity / produced_amount)
    leftovers[out_name] += times_to_run * produced_amount - out_quantity

    total_ore = 0
    for in_name, in_quantity in chemicals_needed:
        in_needed = times_to_run * in_quantity
        total_ore += calculate_ore(reactions, in_needed, in_name, leftovers)

    return total_ore


def part_one(reactions: dict[str, tuple[int, list[tuple[str, int]]]]) -> int:
    return calculate_ore(reactions, 1)


def part_two(reactions: dict[str, tuple[int, list[tuple[str, int]]]]) -> int:
    ore_per_fuel = calculate_ore(reactions, 1)
    available_ore = 1000000000000
    no_reusing = available_ore // ore_per_fuel

    n = no_reusing // 2
    leftover = defaultdict(int)
    fuel = 0
    while True:
        leftover_new = deepcopy(leftover)
        ore = calculate_ore(reactions, n, leftovers=leftover_new)
        if available_ore - ore < 0:
            n = n // 2
            if n == 0:
                break
        else:
            available_ore -= ore
            fuel += n
            leftover = leftover_new
    return fuel


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"

    reactions = {}
    for line in input_path.read_text().splitlines():
        ins, out = line.split(" => ")
        quantity_out, name_out = out.split(" ")
        in_chemicals = []
        for chemical_in in ins.split(", "):
            quantity_in, name_in = chemical_in.split(" ")
            in_chemicals.append((name_in, int(quantity_in)))
        reactions[name_out] = (int(quantity_out), in_chemicals)

    print("FIRST PART", part_one(reactions))
    print("SECOND PART", part_two(reactions))
