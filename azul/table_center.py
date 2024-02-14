# I am using https://github.com/spitalskya/PTS1-Azul .
# This is just so I am able to write integration tests
# ungortunately, here I have to change the .take method.

from __future__ import annotations
from typing import List
from azul.interfaces import GiveTilesInterface, TileSourceInterface
from azul.simple_types import Tile, compress_tile_list, STARTING_PLAYER


class TableCenter(GiveTilesInterface, TileSourceInterface):

    _tiles: List[Tile]

    def __init__(self) -> None:
        self._tiles = []

    def take(self, idx: int) -> List[Tile]:
        """Returns all tiles of corresponding type + STARTING_PLAYER tile if it is in _tiles"""
        try:
            tile_type = self._tiles[idx]
        except IndexError:
            return []
        if tile_type == STARTING_PLAYER:
            return []

        tiles_to_give: List[Tile] = [
            tile for tile in self._tiles if tile == tile_type]
        for tile in tiles_to_give:
            self._tiles.remove(tile)

        if STARTING_PLAYER in self._tiles:
            tiles_to_give.append(STARTING_PLAYER)
            self._tiles.remove(STARTING_PLAYER)

        return tiles_to_give

    def is_empty(self) -> bool:
        return not self._tiles

    def start_new_round(self) -> None:
        """Creates new STARTING_PLAYER tile"""
        assert not self._tiles
        self._tiles.append(STARTING_PLAYER)

    def add(self, tiles: List[Tile]) -> None:
        self._tiles.extend(tiles)

    def state(self) -> str:
        return compress_tile_list(self._tiles)
