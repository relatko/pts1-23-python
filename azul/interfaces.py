from __future__ import annotations
from typing import List
from azul.simple_types import Tile


class UsedTilesGiveInterface:
    def give(self, tiles: List[Tile]) -> None:
        pass
