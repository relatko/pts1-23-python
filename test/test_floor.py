from __future__ import annotations
import unittest
from typing import List
from azul.interfaces import UsedTilesGiveInterface
from azul.simple_types import Tile, STARTING_PLAYER, RED, GREEN, Points
from azul.floor import Floor


class FakeUsedTiles(UsedTilesGiveInterface):
    tiles_given: List[Tile]

    def __init__(self) -> None:
        self.tiles_given = []

    def give(self, tiles: List[Tile]) -> None:
        self.tiles_given.extend(tiles)


class TestFloor(unittest.TestCase):
    def setUp(self) -> None:
        self.used_tiles: FakeUsedTiles = FakeUsedTiles()
        self.floor: Floor = Floor(
            [Points(1), Points(2), Points(2)], self.used_tiles)

    def test_many_tiles(self) -> None:
        tiles = [STARTING_PLAYER, RED, GREEN, RED]
        self.assertCountEqual(self.floor.state(), "")
        self.floor.put(tiles)
        self.assertCountEqual(self.floor.state(), "SRRG")
        points: Points = self.floor.finish_round()
        self.assertEqual(str(points), "7")
        self.assertCountEqual(tiles, self.used_tiles.tiles_given)
        self.assertCountEqual(self.floor.state(), "")


if __name__ == '__main__':
    unittest.main()
