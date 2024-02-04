from __future__ import annotations
import json
from typing import List, Optional, Tuple, Callable
from azul.simple_types import Tile, compress_tile_list, Points
from azul.interfaces import PatternLineWallLineInterface


class WallLine(PatternLineWallLineInterface):
    _line_up: Optional[WallLine]
    _line_down: Optional[WallLine]
    _tile_types: List[Tile]
    _tiles: List[Optional[Tile]]

    def __init__(self, tile_types: List[Tile], tiles: List[Optional[Tile]]):
        assert len(tile_types) == len(tiles)
        self._tile_types = tile_types.copy()
        self._tiles = tiles.copy()
        self._line_up = None
        self._line_down = None

    @property
    def line_up(self) -> Optional[WallLine]:
        return self._line_up

    @line_up.setter
    def line_up(self, line_up: WallLine) -> None:
        assert self._line_up is None
        self._line_up = line_up

    @property
    def line_down(self) -> Optional[WallLine]:
        return self._line_down

    @line_down.setter
    def line_down(self, line_down: WallLine) -> None:
        assert self._line_down is None
        self._line_down = line_down

    @property
    def tiles(self) -> List[Optional[Tile]]:
        return self._tiles.copy()

    def can_put_tile(self, tile: Tile) -> bool:
        return tile not in self._tiles

    def put_tile(self, tile: Tile) -> Points:
        def move_left(line: WallLine, idx: int) -> Optional[Tuple[WallLine, int]]:
            return (line, idx-1) if idx-1 >= 0 else None

        def move_right(line: WallLine, idx: int) -> Optional[Tuple[WallLine, int]]:
            return (line, idx+1) if idx+1 < len(line.tiles) else None

        def move_up(line: WallLine, idx: int) -> Optional[Tuple[WallLine, int]]:
            return (line.line_up, idx) if line.line_up else None

        def move_down(line: WallLine, idx: int) -> Optional[Tuple[WallLine, int]]:
            return (line.line_down, idx) if line.line_down else None

        def search(line: WallLine, idx: int,
                   function: Callable[[WallLine, int], Optional[Tuple[WallLine, int]]]) -> int:
            next_position = function(line, idx)
            if not next_position:
                return 0
            line, idx = next_position
            if not line.tiles[idx]:
                return 0
            return search(line, idx, function) + 1

        idx = self._tile_types.index(tile)
        assert self._tiles[idx] is None
        self._tiles[idx] = tile

        length_x = search(self, idx, move_left) + 1 + \
            search(self, idx, move_right)
        length_y = search(self, idx, move_up) + 1 + \
            search(self, idx, move_down)

        length_less, length_more = sorted([length_x, length_y])
        points_less = length_less if length_less != 1 else 0
        return Points(length_more + points_less)

    def state(self) -> str:
        state = {
            "tile types": compress_tile_list(self._tile_types),
            "tiles": "".join([(compress_tile_list([tile])[0] if tile else " ")
                              for tile in self._tiles]),  # can live with it if I need it just once
        }
        return json.dumps(state)
