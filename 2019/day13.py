import re
import sys
from copy import deepcopy
from enum import Enum
from pathlib import Path

from intcode import IntCodeComputer
from rich.live import Live
from rich.table import Table


def ints_in_str(s: str) -> list[int]:
    return [int(x) for x in re.findall(r"(-?\d+)", s)]


class Tile(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    HORIZONTAL = 3
    BALL = 4


TILE_TO_CHAR = {
    Tile.EMPTY: " ",
    Tile.WALL: "|",
    Tile.BLOCK: "x",
    Tile.HORIZONTAL: "_",
    Tile.BALL: "O",
}


class ArcadeGame:
    DIMENSIONS = 22, 44

    def __init__(self, live=None) -> None:
        self.tiles = {}
        self._x = None
        self._y = None
        self._display = False
        self.score = 0
        self._transformed = False
        self.ball = 0, 0
        self.paddle = 0, 0
        self._live = live
        if self._live:
            self._live.start()

    def get_display(self):
        display = [[" " for _ in range(ArcadeGame.DIMENSIONS[1])] for _ in range(ArcadeGame.DIMENSIONS[0])]
        for (y, x), tile in self.tiles.items():
            display[x][y] = TILE_TO_CHAR[tile]

        table = Table(show_header=False)
        for row in display:
            table.add_row(" ".join(row))
        return table

    def add_tile(self, value: int):
        if self._x is None:
            self._x = value
        elif self._y is None:
            self._y = value
        else:
            if self._x == -1 and self._y == 0:
                self.score = value
            else:
                tile = Tile(value)
                self.tiles[(self._x, self._y)] = tile
                if self._live is not None and len(self.tiles) == self.DIMENSIONS[0] * self.DIMENSIONS[1]:
                    self._live.update(self.get_display(), refresh=True)
                if tile == Tile.BALL:
                    self.ball = self._x, self._y
                elif tile == Tile.HORIZONTAL:
                    self.paddle = self._x, self._y
            self._x, self._y = None, None


def part_one(memory: list[int]) -> int:
    game = ArcadeGame()
    computer = IntCodeComputer(deepcopy(memory), lambda: None, game.add_tile)
    computer.run_intcode()
    return sum(1 for tile in game.tiles.values() if tile == Tile.BLOCK)


def part_two(memory: list[int]) -> int:
    memory[0] = 2
    watch = True  # Make false if you dont' want to watch it play out
    live = Live() if watch else None
    game = ArcadeGame(live)

    def choose_move():
        if game.ball[0] == game.paddle[0]:
            return 0
        elif game.ball[0] > game.paddle[0]:
            return 1
        else:
            return -1

    computer = IntCodeComputer(deepcopy(memory), choose_move, game.add_tile)
    computer.run_intcode()
    if live is not None:
        live.stop()

    return game.score


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"

    memory = ints_in_str(input_path.read_text())

    print("FIRST PART", part_one(memory))
    print("SECOND PART", part_two(memory))
