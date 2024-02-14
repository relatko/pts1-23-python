from __future__ import annotations
from typing import List, Optional
from azul.interfaces import FinalPointsCalculationInterface
from azul.simple_types import Tile, Points


class FinalPointsCalculation(FinalPointsCalculationInterface):
    def get_points(self, wall: List[List[Optional[Tile]]]) -> Points:
        assert len(wall) == 5
        assert all([len(line) == 5 for line in wall])
        row_points: int = sum([(2 if all(line) else 0) for line in wall])
        transposed_wall = list(zip(*wall))
        column_points: int = sum([(7 if all(line) else 0)
                                  for line in transposed_wall])
        color_points: int = 10 * \
            len(set.intersection(
                *[{tile for tile in line if tile} for line in wall]))
        return Points(row_points + column_points + color_points)
