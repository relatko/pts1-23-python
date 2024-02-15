from __future__ import annotations
import json
from typing import List, Optional, Any
from azul.interfaces import BoardInterface
from azul.interfaces import (FinalPointsCalculationInterface, GameFinishedInterface,
                             WallLineInterface, PatternLineInterface, FloorInterface)
from azul.simple_types import Tile, FinishRoundResult, Points


class Board(BoardInterface):
    _points: Points
    _game_finished: GameFinishedInterface
    _final_points_calculation: FinalPointsCalculationInterface
    _pattern_lines: List[PatternLineInterface]
    _wall_lines: List[WallLineInterface]
    _floor: FloorInterface

    def __init__(self, game_finished: GameFinishedInterface,
                 final_points: FinalPointsCalculationInterface,
                 pattern_lines: List[PatternLineInterface],
                 wall_line: List[WallLineInterface],
                 floor: FloorInterface) -> None:
        # pylint: disable=too-many-arguments
        self._points = Points(0)
        self._game_finished = game_finished
        self._final_points_calculation = final_points
        self._pattern_lines = pattern_lines.copy()
        self._wall_lines = wall_line.copy()
        self._floor = floor

    @property
    def points(self) -> Points:
        return self._points

    def _get_wall(self) -> List[List[Optional[Tile]]]:
        return [wall_line.tiles for wall_line in self._wall_lines]

    def put(self, destination_idx: int, tiles: List[Tile]) -> None:
        """Puts tile to PatternLine.
        :destination: 0 to 4 (top to bottom)
        :tiles: list of tiles to put"""
        self._pattern_lines[destination_idx].give(tiles)

    def finish_round(self) -> FinishRoundResult:
        """Adds points from pattern line, negative points from floor
        and current points from board.
        Returns whether end game occurred"""
        line_points = [pattern_line.finish_round()
                       for pattern_line in self._pattern_lines]
        floor_points = self._floor.finish_round()
        self._points = Points.sum_nonnegative(
            line_points + [floor_points, self.points])
        return self._game_finished.game_finished(self._get_wall())

    def end_game(self) -> None:
        """Sums all bonus points from WallLines + current points"""
        final_points: Points = self._final_points_calculation.get_points(
            self._get_wall())
        self._points = Points.sum([self._points, final_points])

    def _state(self) -> str:
        state: Any = {
            "points": self._points.value,
            "pattern lines": [json.loads(line.state()) for line in self._pattern_lines],
            "wall lines": [json.loads(line.state()) for line in self._wall_lines],
        }
        return json.dumps(state)
