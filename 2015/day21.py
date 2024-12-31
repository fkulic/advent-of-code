import math
import re
import sys
from collections import namedtuple
from itertools import combinations
from pathlib import Path


def ints_in_str(s: str) -> list[int]:
    return [int(x) for x in re.findall(r"(-?\d+)", s)]


Player = namedtuple("Player", ["hp", "damage", "armor"])
Item = namedtuple("Item", ["cost", "damage", "armor"])


def get_dmg(player1_dmg: int, player2_armor: int) -> int:
    dmg = player1_dmg - player2_armor
    if dmg < 1:
        return 1
    return dmg


def make_player(weapon: Item, armor: Item, ring1: Item, ring2: Item) -> Player:
    return Player(100, weapon.damage + ring1.damage + ring2.damage, armor.armor + ring1.armor + ring2.armor)


def fight(player1: Player, player2: Player):
    # True if player 1 wins, False if player 2 wins
    p1_dmg = get_dmg(player1.damage, player2.armor)
    p2_dmg = get_dmg(player2.damage, player1.armor)
    p1_strikes_needed = math.ceil(player2.hp / p1_dmg)
    p2_strikes_needed = math.ceil(player1.hp / p2_dmg)
    return p1_strikes_needed <= p2_strikes_needed


def both_parts(enemy: Player, weapons: list[Item], armors: list[Item], rings: list[Item]) -> tuple[int, int]:
    no_item = Item(0, 0, 0)
    armors.append(no_item)
    rings.extend([no_item, no_item])

    min_cost_won = 2000
    max_cost_lost = 0
    for w in weapons:
        for a in armors:
            for r1, r2 in combinations(rings, 2):
                player = make_player(w, a, r1, r2)
                cost = w.cost + a.cost + r1.cost + r2.cost
                if fight(player, enemy):
                    min_cost_won = min(cost, min_cost_won)
                else:
                    max_cost_lost = max(cost, max_cost_lost)

    return min_cost_won, max_cost_lost


if __name__ == "__main__":
    assert len(sys.argv) > 2, "No input paths"

    input_path = Path(sys.argv[1])
    assert input_path.is_file(), "Puzzle input path is not a file"

    shop_input_path = Path(sys.argv[2])  # Input for what shop is selling
    assert shop_input_path.is_file(), "Shop input path is not a file"

    data = []
    for line in input_path.read_text().splitlines():
        data.append(int(line.split(": ")[1]))

    weapons, armors, rings = shop_input_path.read_text().split("\n\n")
    read_items = lambda x: [Item(*ints_in_str(line)) for line in x.splitlines()[1:]]

    weapons = read_items(weapons)
    armors = read_items(armors)
    rings = [Item(*ints_in_str(line)[1:]) for line in rings.splitlines()[1:]]

    enemy = Player(*data)

    first, second = both_parts(enemy, weapons, armors, rings)
    print("FIRST PART", first)
    print("SECOND PART", second)
