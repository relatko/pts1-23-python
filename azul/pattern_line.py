from __future__ import annotations
import json
from typing import List
from azul.simple_types import Tile, compress_tile_list, Points, STARTING_PLAYER
from azul.interfaces import (FloorInterface, GiveTilesInterface, PatternLineWallLineInterface,
                             PatternLineInterface)


class PatternLine(PatternLineInterface):
    _floor: FloorInterface
    _used_tiles: GiveTilesInterface
    _wall_line: PatternLineWallLineInterface
    _capacity: int
    _tiles: List[Tile]

    def __init__(self, capacity: int, floor: FloorInterface,
                 used_tiles: GiveTilesInterface, wall_line: PatternLineWallLineInterface):
        assert capacity != 0
        self._capacity = capacity
        self._floor = floor
        self._used_tiles = used_tiles
        self._wall_line = wall_line
        self._tiles = []

    def give(self, tiles: List[Tile]) -> None:
        # Drop starting player stone to the floor
        self._floor.give([tile for tile in tiles if tile == STARTING_PLAYER])
        tiles = [tile for tile in tiles if tile != STARTING_PLAYER]

        # Check if tiles are all of the same type
        if not tiles:
            return
        assert all([tile == tiles[0] for tile in tiles])

        assert self._capacity >= len(self._tiles)
        count_to_fit = min(self._capacity - len(self._tiles), len(tiles))

        if self._tiles:
            if self._tiles[0] == tiles[0]:
                count_to_put = count_to_fit
            else:
                count_to_put = 0
        else:
            if self._wall_line.can_put_tile(tiles[0]):
                count_to_put = count_to_fit
            else:
                count_to_put = 0

        self._tiles.extend(tiles[0:count_to_put])
        self._floor.give(tiles[count_to_put:])

    def finish_round(self) -> Points:
        if len(self._tiles) == self._capacity:
            assert len(self._tiles) != 0
            assert self._wall_line.can_put_tile(self._tiles[0])
            self._used_tiles.give(self._tiles[1:])
            points_floor = self._floor.finish_round()
            points_wall = self._wall_line.put_tile(self._tiles[0])
            self._tiles = []
            return Points.sum([points_floor, points_wall])
        return Points(0)

    def state(self) -> str:
        state = {
            "tiles": compress_tile_list(self._tiles),
            "capacity": self._capacity,
        }
        return json.dumps(state)
