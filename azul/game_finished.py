from __future__ import annotations
from typing import List, Optional
from azul.interfaces import GameFinishedInterface
from azul.simple_types import Tile, FinishRoundResult


class GameFinished(GameFinishedInterface):

    def game_finished(self, wall: List[List[Optional[Tile]]]) -> FinishRoundResult:
        """Determines whether game should end

        Gets board wall state as a 2D list as an argument
        """
        line: List[Optional[Tile]]
        for line in wall:
            if None not in line:
                return FinishRoundResult.GAME_FINISHED

        return FinishRoundResult.NORMAL
