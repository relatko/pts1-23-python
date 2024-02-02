from typing import List
from azul.simple_types import Tile
from azul.interfaces import GiveTilesInterface


class FakeGiveTiles(GiveTilesInterface):
    tiles_given: List[Tile]

    def __init__(self) -> None:
        self.tiles_given = []

    def give(self, tiles: List[Tile]) -> None:
        self.tiles_given.extend(tiles)
