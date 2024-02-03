from __future__ import annotations
from typing import List
from azul.simple_types import Tile, FinishRoundResult, Points


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


class GameInterface:
    def start_game(self) -> None:
        pass

    def take(self, player_id: int, source_idx: int, idx: int, destination_idx: int) -> bool:
        pass


class TableCenterInterface(StateInterface):
    def take(self, source_idx: int, idx: int) -> List[Tile]:
        pass

    def is_round_end(self) -> bool:
        pass

    def start_new_round(self) -> None:
        pass


class BoardInterface(StateInterface):
    def put(self, destination_idx: int, tiles: List[Tile]) -> None:
        pass

    def finish_round(self) -> FinishRoundResult:
        pass

    def end_game(self) -> None:
        pass


class NotifyEverybodyInterface:
    def notify_everybody(self, state: str) -> None:
        pass


class FloorInterface(StateInterface, GiveTilesInterface):
    def finish_round(self) -> Points:
        pass
