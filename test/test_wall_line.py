from __future__ import annotations
import unittest
import json
from typing import Any, List, Optional
from azul.simple_types import BLUE, RED, GREEN, Tile
from azul.wall_line import WallLine


class TestWallLine(unittest.TestCase):
    def setUp(self) -> None:
        tile_types = [RED, GREEN, BLUE]
        tiles: List[Optional[Tile]] = [None, None, None]
        self.wall_line1 = WallLine(tile_types, tiles)
        self.wall_line2 = WallLine(tile_types, tiles)
        self.wall_line3 = WallLine(tile_types, tiles)
        self.wall_line1.line_down = self.wall_line2
        self.wall_line2.line_down = self.wall_line3
        self.wall_line3.line_up = self.wall_line2
        self.wall_line2.line_up = self.wall_line1

    @staticmethod
    def state(wall_line: WallLine) -> Any:
        return json.loads(wall_line.state())

    def test_can_put_tiles(self) -> None:
        self.assertTrue(self.wall_line1.can_put_tile(RED))
        self.wall_line1.put_tile(RED)
        self.assertFalse(self.wall_line1.can_put_tile(RED))
        self.assertTrue(self.wall_line1.can_put_tile(BLUE))

    def test_cannot_put_tile_twice(self) -> None:
        self.wall_line1.put_tile(RED)
        with self.assertRaises(AssertionError):
            self.wall_line1.put_tile(RED)

    def test_points_one_x_one(self) -> None:
        self.assertEqual(self.wall_line1.put_tile(RED).value, 1)

    def test_points_one_x_many(self) -> None:
        self.assertEqual(self.wall_line1.put_tile(GREEN).value, 1)
        self.assertEqual(self.wall_line1.put_tile(BLUE).value, 2)
        self.assertEqual(self.wall_line1.put_tile(RED).value, 3)

    def test_points_many_x_one(self) -> None:
        self.assertEqual(self.wall_line2.put_tile(BLUE).value, 1)
        self.assertEqual(self.wall_line1.put_tile(BLUE).value, 2)
        self.assertEqual(self.wall_line3.put_tile(BLUE).value, 3)

    def test_points_many_x_many(self) -> None:
        self.assertEqual(self.wall_line2.put_tile(BLUE).value, 1)
        self.assertEqual(self.wall_line1.put_tile(BLUE).value, 2)
        self.assertEqual(self.wall_line2.put_tile(GREEN).value, 2)
        # _ _ B
        # _ G B
        # _ _ _
        self.assertEqual(self.wall_line3.put_tile(BLUE).value, 3)
        self.assertEqual(self.wall_line2.put_tile(RED).value, 3)
        self.assertEqual(self.wall_line3.put_tile(GREEN).value, 4)
        # _ _ B
        # R G B
        # _ G B
        self.assertEqual(self.wall_line1.put_tile(RED).value, 2)
        self.assertEqual(self.wall_line1.put_tile(GREEN).value, 6)
        self.assertEqual(self.wall_line3.put_tile(RED).value, 6)

    def test_state(self) -> None:
        self.wall_line2.put_tile(BLUE)
        self.assertEqual(TestWallLine.state(self.wall_line2)["tiles"], "  B")
        self.assertEqual(TestWallLine.state(
            self.wall_line2)["tile types"], "RGB")


if __name__ == '__main__':
    unittest.main()
