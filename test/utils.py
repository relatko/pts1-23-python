from typing import List, Tuple
from azul.simple_types import Tile, RED, GREEN, BLACK, BLUE, YELLOW
from azul.interfaces import GiveTilesInterface
from azul.bag import Bag


class FakeGiveTiles(GiveTilesInterface):
    tiles_given: List[Tile]

    def __init__(self) -> None:
        self.tiles_given = []

    def give(self, tiles: List[Tile]) -> None:
        self.tiles_given.extend(tiles)


class FakeShuffler(Bag.RandomTakeInterface):
    next_take: List[List[Tile]]

    def __init__(self) -> None:
        self.next_take = []

    def take(self, count: int, tiles: List[Tile]) -> Tuple[List[Tile], List[Tile]]:
        if not count:
            return ([], tiles)
        assert self.next_take
        we_want = self.next_take[0]
        self.next_take = self.next_take[1:]
        assert len(we_want) == count

        for tile in we_want:
            assert tile in tiles
            tiles.remove(tile)

        return we_want, tiles

    def instructions(self, draws: List[str]) -> None:
        assert not self.next_take
        convert = {"R": RED, "G": GREEN, "B": BLUE, "L": BLACK, "Y": YELLOW}
        for draw in draws:
            self.next_take.append([convert[c] for c in draw])
