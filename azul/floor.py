from __future__ import annotations
import json
from typing import List
from itertools import chain, repeat, islice
from azul.interfaces import GiveTilesInterface, FloorInterface
from azul.simple_types import Tile, compress_tile_list, Points


class Floor(FloorInterface):
    _point_pattern: List[Points]
    _used_tiles: GiveTilesInterface
    _tiles: List[Tile]

    def __init__(self, point_pattern: List[Points], used_tiles: GiveTilesInterface):
        self._point_pattern = point_pattern.copy()
        self._used_tiles = used_tiles
        self._tiles = []

    def give(self, tiles: List[Tile]) -> None:
        self._tiles.extend(tiles)

    def finish_round(self) -> Points:
        extended_pattern = chain(
            self._point_pattern, repeat(self._point_pattern[-1]))
        points: Points = Points.sum(
            list(islice(extended_pattern, 0, len(self._tiles))))
        self._used_tiles.give(self._tiles.copy())
        self._tiles = []
        return points

    def state(self) -> str:
        return json.dumps(compress_tile_list(self._tiles))
