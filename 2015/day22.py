import random
import sys
from copy import deepcopy
from enum import Enum
from pathlib import Path


class Spell(Enum):
    MAGIC_MISSLE = 1
    DRAIN = 2
    SHIELD = 3
    POISON = 4
    RECHARGE = 5


SHIELD_ARMOR = 7
POISON_DMG = 3
RECHARGE_MANA = 101

SPELL_COST = {
    Spell.MAGIC_MISSLE: 53,
    Spell.DRAIN: 73,
    Spell.SHIELD: 113,
    Spell.POISON: 173,
    Spell.RECHARGE: 229,
}


class Player:
    def __init__(self, hp: int, mana: int) -> None:
        self.hp = hp
        self.mana = mana
        self.shield = 0
        self.recharge = 0
        self.total_mana_used = 0

    def cast(self, spell: Spell, enemy: "Boss") -> None:
        self.mana -= SPELL_COST[spell]
        self.total_mana_used += SPELL_COST[spell]
        match spell:
            case Spell.MAGIC_MISSLE:
                enemy.hp -= 4
            case Spell.DRAIN:
                enemy.hp -= 2
                self.hp += 2
            case Spell.SHIELD:
                self.shield = 6
            case Spell.POISON:
                enemy.posion = 6
            case Spell.RECHARGE:
                self.recharge = 5

    def __repr__(self) -> str:
        return f"{self.hp=} {self.mana=} {self.shield=} {self.recharge=}"

    def can_cast(self, enemy: "Boss") -> list[Spell]:
        spells = [Spell.MAGIC_MISSLE, Spell.DRAIN]
        if self.shield in (0, 1):
            spells.append(Spell.SHIELD)
        if self.recharge in (0, 1):
            spells.append(Spell.RECHARGE)
        if enemy.posion in (0, 1):
            spells.append(Spell.POISON)
        return [spell for spell in spells if self.mana >= SPELL_COST[spell]]


class Boss:
    def __init__(self, hp: int, damage: int) -> None:
        self.hp = hp
        self.damage = damage
        self.posion = 0

    def __repr__(self) -> str:
        return f"{self.hp=} {self.posion=}"

    def attack(self, player: Player) -> None:
        if player.shield != 0:
            dmg = self.damage - SHIELD_ARMOR
            player.shield -= 2
            if dmg < 1:
                player.hp -= 1
            else:
                player.hp -= dmg
        else:
            player.hp -= self.damage


def apply_effects(player: Player, boss: Boss) -> None:
    if boss.posion != 0:
        boss.hp -= POISON_DMG
        boss.posion -= 1
    if player.recharge != 0:
        player.mana += RECHARGE_MANA
        player.recharge -= 1


def hard_mode_player_died(player: Player) -> bool:
    player.hp -= 1
    return player.hp <= 0


def fight(player: Player, boss: Boss, hard: bool = False) -> bool:
    while True:
        if hard:
            if hard_mode_player_died(player):
                return False

        apply_effects(player, boss)
        if boss.hp <= 0:
            return True

        spells = player.can_cast(boss)
        if len(spells) == 0:
            return False

        player.cast(random.choice(spells), boss)
        if boss.hp <= 0:
            return True

        apply_effects(player, boss)
        boss.attack(player)
        if player.hp <= 0:
            return False


def fight_n_times(boss: Boss, n: int, hard: bool) -> int:
    min_mana = 1000000
    for _ in range(n):
        player = Player(50, 500)
        if fight(player, deepcopy(boss), hard):
            min_mana = min(min_mana, player.total_mana_used)
    return min_mana


def part_one(boss: Boss) -> int:
    return fight_n_times(boss, 10000, hard=False)


def part_two(boss: Boss) -> int:
    return fight_n_times(boss, 50000, hard=True)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"

    input_path = Path(sys.argv[1])
    assert input_path.is_file(), "Puzzle input path is not a file"

    data = [int(line.split(": ")[1]) for line in input_path.read_text().splitlines()]
    boss = Boss(*data)

    print("FIRST PART", part_one(boss))
    print("SECOND PART", part_two(boss))
