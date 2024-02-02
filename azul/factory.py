from __future__ import annotations
from typing import List, Final, Callable
from azul.interfaces import TileSourceInterface, GiveTilesInterface, TakeTilesFromBagInterface
from azul.simple_types import Tile, compress_tile_list


class Factory(TileSourceInterface):
    _bag: TakeTilesFromBagInterface
    _table_center: GiveTilesInterface
    _tiles: List[Tile]
    MAX_NUMBER_OF_TILES: Final = 4

    def __init__(self, bag: TakeTilesFromBagInterface, center: GiveTilesInterface):
        self._bag = bag
        self._table_center = center
        self._tiles = []

    def take(self, idx: int) -> List[Tile]:
        try:
            tile = self._tiles[idx]
        except IndexError:
            return []
        current_list = self._tiles
        self._tiles = []
        take_condition: Callable[[Tile], bool] = lambda x: x == tile
        to_take = [x for x in current_list if take_condition(x)]
        to_center = [x for x in current_list if not take_condition(x)]
        self._table_center.give(to_center)
        return to_take

    def is_empty(self) -> bool:
        return not self._tiles

    def start_new_round(self) -> None:
        assert not self._tiles
        self._tiles = self._bag.take(Factory.MAX_NUMBER_OF_TILES)

    def state(self) -> str:
        return compress_tile_list(self._tiles)
