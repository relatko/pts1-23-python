from typing import List, Tuple, Dict
from azul.simple_types import Tile
from azul.interfaces import GiveTilesInterface
from azul.bag import Bag


class FakeGiveTiles(GiveTilesInterface):
    tiles_given: List[Tile]

    def __init__(self) -> None:
        self.tiles_given = []

    def give(self, tiles: List[Tile]) -> None:
        self.tiles_given.extend(tiles)


class FakeShuffler(Bag.RandomTakeInterface):
    next_take: Dict[str, List[Tile]]

    def take(self, count: int, for_whom: str,
             tiles: List[Tile]) -> Tuple[List[Tile], List[Tile]]:
        we_want = self.next_take[for_whom]
        print(we_want)
        print(count)
        assert len(we_want) == count

        for tile in we_want:
            assert tile in tiles
            tiles.remove(tile)

        return we_want, tiles
