# I am using https://github.com/spitalskya/PTS1-Azul .
# This is just so I am able to write integration tests

from __future__ import annotations
from typing import List
import json
from azul.simple_types import Tile, STARTING_PLAYER, compress_tile_list
from azul.interfaces import BagUsedTilesInterface, GiveTilesInterface


class UsedTiles(BagUsedTilesInterface, GiveTilesInterface):
    """Stores used tiles from Floor and PatternLine to by taken by Bag"""

    _tiles: List[Tile]

    def __init__(self) -> None:
        self._tiles = []

    def give(self, tiles: List[Tile]) -> None:
        """Takes list of tiles, removes STARTING_PLAYER and extends _tiles with the rest"""
        if STARTING_PLAYER in tiles:
            tiles.remove(STARTING_PLAYER)
        self._tiles.extend(tiles)

    def take_all(self) -> List[Tile]:
        """Returns whole _tiles list and clears it"""
        new_copy: List[Tile] = self._tiles.copy()
        self._tiles.clear()
        return new_copy

    def state(self) -> str:
        return json.dumps(compress_tile_list(self._tiles))

    def get_tiles(self) -> List[Tile]:
        return self._tiles
