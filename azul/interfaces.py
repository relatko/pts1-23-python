from __future__ import annotations
from typing import List, Optional
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


class TableAreaInterface(StateInterface):
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


class PatternLineWallLineInterface:
    def can_put_tile(self, tile: Tile) -> bool:
        pass

    def put_tile(self, tile: Tile) -> Points:
        pass


class ObserverInterface:
    def notify(self, new_state: str) -> None:
        pass


class ObservableInterface:
    def register_observer(self, observer: ObserverInterface) -> None:
        pass

    def cancel_observer(self, observer: ObserverInterface) -> None:
        pass


class FinalPointsCalculationInterface:
    def get_points(self, wall: List[List[Optional[Tile]]]) -> Points:
        pass


class GameFinishedInterface:
    def game_finished(self, wall: List[List[Optional[Tile]]]) -> FinishRoundResult:
        pass


class WallLineInterface(StateInterface):
    @property
    def tiles(self) -> List[Optional[Tile]]:
        pass


class PatternLineInterface(StateInterface, GiveTilesInterface):
    def finish_round(self) -> Points:
        pass
