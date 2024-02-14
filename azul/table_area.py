# I am using https://github.com/spitalskya/PTS1-Azul .
# This is just so I am able to write integration tests

from __future__ import annotations
from typing import List, Any
import json
from azul.interfaces import TableAreaInterface, TileSourceInterface
from azul.simple_types import Tile


class TableArea(TableAreaInterface):

    _table_center: TileSourceInterface
    _factories: List[TileSourceInterface]

    def __init__(self, factories: List[TileSourceInterface],
                 table_center: TileSourceInterface) -> None:
        self._factories = factories.copy()
        self._table_center = table_center

    def take(self, source_idx: int, idx: int) -> List[Tile]:
        """Calls take() on corresponding tile source"""
        try:
            source: TileSourceInterface = (
                [self._table_center]+self._factories)[source_idx]
        except IndexError:
            return []
        return source.take(idx)

    def is_round_end(self) -> bool:
        """Checks if all tile sources are empty"""
        return all(tile_source.is_empty() for tile_source in self._factories+[self._table_center])

    def start_new_round(self) -> None:
        """Calls start_new_round() on all tile sources"""
        # TableArea has to call Factories in the order of their of their indices.
        for tile_source in self._factories:
            tile_source.start_new_round()
        self._table_center.start_new_round()

    def state(self) -> str:
        state: Any = {
            "factories": [json.loads(factory.state()) for factory in self._factories],
            "table center": json.loads(self._table_center.state()),
        }
        return json.dumps(state)
