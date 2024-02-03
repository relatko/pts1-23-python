from __future__ import annotations
from typing import List
from azul.simple_types import Tile


class GiveTilesInterface:
    def give(self, tiles: List[Tile]) -> None:
        pass


class TakeTilesFromBagInterface:
    def take(self, count: int) -> List[Tile]:
        pass


class StateInterface:
    def state(self) -> str:
        pass


class BagUsedTilesInterface(StateInterface):
    def take_all(self) -> List[Tile]:
        pass


class TileSourceInterface:
    def take(self, idx: int) -> List[Tile]:
        pass

    def is_empty(self) -> bool:
        pass

    def start_new_round(self) -> None:
        pass

    def state(self) -> str:
        pass
