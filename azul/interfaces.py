# pylint: disable=unused-argument
from __future__ import annotations
from typing import List, Optional
from azul.simple_types import Tile, FinishRoundResult, Points


class GiveTilesInterface:
    def give(self, tiles: List[Tile]) -> None:
        assert False


class TakeTilesFromBagInterface:
    def take(self, count: int) -> List[Tile]:
        assert False


class StateInterface:
    def state(self) -> str:
        assert False


class BagUsedTilesInterface(StateInterface):
    def take_all(self) -> List[Tile]:
        assert False


class TileSourceInterface:
    def take(self, idx: int) -> List[Tile]:
        assert False

    def is_empty(self) -> bool:
        assert False

    def start_new_round(self) -> None:
        assert False

    def state(self) -> str:
        assert False


class GameInterface:
    def start_game(self) -> None:
        assert False

    def take(self, player_id: int, source_idx: int, idx: int, destination_idx: int) -> bool:
        assert False


class TableAreaInterface(StateInterface):
    def take(self, source_idx: int, idx: int) -> List[Tile]:
        assert False

    def is_round_end(self) -> bool:
        assert False

    def start_new_round(self) -> None:
        assert False


class BoardInterface(StateInterface):
    def put(self, destination_idx: int, tiles: List[Tile]) -> None:
        assert False

    def finish_round(self) -> FinishRoundResult:
        assert False

    def end_game(self) -> None:
        assert False


class NotifyEverybodyInterface:
    def notify_everybody(self, state: str) -> None:
        assert False


class FloorInterface(StateInterface, GiveTilesInterface):
    def finish_round(self) -> Points:
        assert False


class PatternLineWallLineInterface:
    def can_put_tile(self, tile: Tile) -> bool:
        assert False

    def put_tile(self, tile: Tile) -> Points:
        assert False


class ObserverInterface:
    def notify(self, new_state: str) -> None:
        assert False


class ObservableInterface:
    def register_observer(self, observer: ObserverInterface) -> None:
        assert False

    def cancel_observer(self, observer: ObserverInterface) -> None:
        assert False


class FinalPointsCalculationInterface:
    def get_points(self, wall: List[List[Optional[Tile]]]) -> Points:
        assert False


class GameFinishedInterface:
    def game_finished(self, wall: List[List[Optional[Tile]]]) -> FinishRoundResult:
        assert False


class WallLineInterface(StateInterface):
    @property
    def tiles(self) -> List[Optional[Tile]]:
        assert False


class PatternLineInterface(StateInterface, GiveTilesInterface):
    def finish_round(self) -> Points:
        assert False
