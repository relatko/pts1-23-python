from __future__ import annotations
import unittest
import json
from typing import Any
from test.utils import FakeGiveTiles
from azul.simple_types import STARTING_PLAYER, RED, GREEN, Points
from azul.floor import Floor


class TestFloor(unittest.TestCase):
    def setUp(self) -> None:
        self.used_tiles: FakeGiveTiles = FakeGiveTiles()
        self.floor: Floor = Floor(
            [Points(1), Points(2), Points(2)], self.used_tiles)

    def state(self) -> Any:
        return json.loads(self.floor.state())

    def test_tiles(self) -> None:
        tiles = [STARTING_PLAYER, RED, GREEN, RED]
        self.assertCountEqual(self.state(), "")
        self.floor.put(tiles)
        self.assertCountEqual(self.state(), "SRRG")
        points: Points = self.floor.finish_round()
        self.assertEqual(str(points), "7")
        self.assertCountEqual(tiles, self.used_tiles.tiles_given)
        self.assertCountEqual(self.state(), "")
        tiles2 = [RED, GREEN]
        self.floor.put(tiles2[0:1])
        self.assertCountEqual(self.state(), "R")
        self.floor.put(tiles2[1:2])
        self.assertCountEqual(self.state(), "RG")
        self.floor.put([])
        self.assertCountEqual(self.state(), "RG")
        points2: Points = self.floor.finish_round()
        self.assertEqual(str(points2), "3")
        self.assertCountEqual(tiles+tiles2, self.used_tiles.tiles_given)
        self.assertEqual(self.state(), "")


if __name__ == '__main__':
    unittest.main()
