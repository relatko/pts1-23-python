from __future__ import annotations
import unittest
import json
from typing import Any
from test.utils import FakeGiveTiles
from azul.simple_types import STARTING_PLAYER, RED, GREEN, Points, Tile, compress_tile_list
from azul.floor import Floor
from azul.pattern_line import PatternLine
from azul.interfaces import PatternLineWallLineInterface


class FakeWallLine(PatternLineWallLineInterface):
    next_answer: bool
    next_points: int
    last_tile_asked: Tile
    last_tile_put: Tile

    def can_put_tile(self, tile: Tile) -> bool:
        self.last_tile_asked = tile
        return self.next_answer

    def put_tile(self, tile: Tile) -> Points:
        self.last_tile_put = tile
        return Points(self.next_points)


class TestPatternLine(unittest.TestCase):
    def setUp(self) -> None:
        self.used_tiles: FakeGiveTiles = FakeGiveTiles()
        self.floor: Floor = Floor(
            [Points(-1), Points(-2), Points(-2)], self.used_tiles)
        self.wall_line = FakeWallLine()
        self.wall_line.next_answer = True
        self.wall_line.next_points = 1
        self.pattern_line = PatternLine(
            3, self.floor, self.used_tiles, self.wall_line)

    def state(self) -> Any:
        return json.loads(self.pattern_line.state())

    def floor_state(self) -> Any:
        return json.loads(self.floor.state())

    def test_starting_player_drops(self) -> None:
        self.pattern_line.give([RED, STARTING_PLAYER])
        self.assertCountEqual(self.state()["tiles"], "R")
        self.assertCountEqual(self.floor_state(), "S")

    def test_can_add_same_tile_several_times_adding_more_drops(self) -> None:
        self.pattern_line.give([RED, RED])
        self.assertCountEqual(self.state()["tiles"], "RR")
        self.assertCountEqual(self.floor_state(), "")
        self.pattern_line.give([RED, RED])
        self.assertCountEqual(self.state()["tiles"], "RRR")
        self.assertCountEqual(self.floor_state(), "R")

    def test_adding_more_than_capacity_drops(self) -> None:
        self.pattern_line.give(10*[RED])
        self.assertCountEqual(self.state()["tiles"], "RRR")
        self.assertCountEqual(self.floor_state(), "RRRRRRR")

    def test_puting_of_type_not_on_the_line_drops(self) -> None:
        self.pattern_line.give([RED, RED])
        self.pattern_line.give([STARTING_PLAYER, GREEN])
        self.assertCountEqual(self.state()["tiles"], "RR")
        self.assertCountEqual(self.floor_state(), "SG")

    def test_puting_tiles_not_allowed_by_walline_drops(self) -> None:
        self.wall_line.next_answer = False
        self.pattern_line.give([STARTING_PLAYER, RED, RED])
        self.assertEqual(self.wall_line.last_tile_asked, RED)
        self.assertCountEqual(self.state()["tiles"], "")
        self.assertCountEqual(self.floor_state(), "SRR")

    def test_finish_round_works_when_line_not_full(self) -> None:
        self.pattern_line.give([STARTING_PLAYER, RED, RED])
        self.assertEqual(self.pattern_line.finish_round().value, 0)
        self.assertCountEqual(self.state()["tiles"], "RR")
        self.assertCountEqual(self.floor_state(), "S")
        self.assertCountEqual(self.used_tiles.tiles_given, [])

    def test_finish_round_works_when_line_is_full(self) -> None:
        self.pattern_line.give([STARTING_PLAYER, RED, RED])
        self.pattern_line.give([RED, RED])
        self.assertCountEqual(self.floor_state(), "SR")
        self.assertEqual(self.pattern_line.finish_round().value, -2)
        self.assertCountEqual(self.state()["tiles"], "")
        self.assertCountEqual(self.floor_state(), "")
        self.assertEqual(self.wall_line.last_tile_put, RED)
        # Two from line one from floor + starting player
        self.assertCountEqual(compress_tile_list(
            self.used_tiles.tiles_given), "RRRS")

    def test_two_stones_of_different_colors_cause_error(self) -> None:
        with self.assertRaises(AssertionError):
            self.pattern_line.give([GREEN, RED])


if __name__ == '__main__':
    unittest.main()
