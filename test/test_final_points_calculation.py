from __future__ import annotations
import unittest
from typing import List, Optional
from azul.simple_types import Tile, RED, BLUE, YELLOW, GREEN, BLACK
from azul.final_points_calculation import FinalPointsCalculation


class TestFinalPointsCalculation(unittest.TestCase):

    def setUp(self) -> None:
        self.final_points_calculation = FinalPointsCalculation()

    def test_get_points(self) -> None:
        test_wall: List[List[Optional[Tile]]] = [
            [None,  YELLOW, RED,    None,   None],
            [None,  BLUE,   YELLOW, RED,    None],
            [None,  GREEN,  BLUE,   None,   RED],
            [RED,   BLACK,  GREEN,  BLUE,   YELLOW],
            [None,  RED,    BLACK,  GREEN,  None],
        ]
        # 1x2 for line, 2x7 for column and 1x10 for color
        self.assertEqual(
            self.final_points_calculation.get_points(test_wall).value, 26)

    def test_get_points2(self) -> None:
        test_wall: List[List[Optional[Tile]]] = [
            [BLUE,   YELLOW, RED,    BLACK,  GREEN],
            [GREEN,  BLUE,   YELLOW, RED,    BLACK],
            [BLACK,  GREEN,  BLUE,   YELLOW, RED],
            [RED,    None,   None,   BLUE,   None],
            [YELLOW, None,   None,   None,   None],
        ]
        # 3x2 for line, 1x7 for column and 0x10 for color
        self.assertEqual(
            self.final_points_calculation.get_points(test_wall).value, 13)

    def test_get_points3(self) -> None:
        test_wall: List[List[Optional[Tile]]] = [
            [BLUE,  None,  RED,    BLACK,  GREEN],
            [GREEN, BLUE,  YELLOW, None,   BLACK],
            [BLACK, GREEN, None,   YELLOW, RED],
            [None,  BLACK, GREEN,  None,   None],
            [None,  None,  None,   None,   None],
        ]
        self.assertEqual(
            self.final_points_calculation.get_points(test_wall).value, 0)
