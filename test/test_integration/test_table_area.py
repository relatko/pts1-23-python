from __future__ import annotations
import unittest
import json
from typing import Any, List
from test.utils import FakeShuffler
from azul.simple_types import Tile, RED, GREEN, BLUE, YELLOW, STARTING_PLAYER
from azul.factories import create_table_area


class TestTableArea(unittest.TestCase):
    def setUp(self) -> None:
        self.shuffler: FakeShuffler = FakeShuffler()
        self.table_area, self.bag, self.used_tiles = \
            create_table_area(3, self.shuffler, 10*(RED, GREEN, BLUE, YELLOW))
        self.shuffler.next_take = [
            [RED, RED, RED, RED],
            [GREEN, GREEN, GREEN, BLUE],
            [YELLOW, GREEN, GREEN, GREEN],
            [GREEN, GREEN, GREEN, GREEN],
            [RED, BLUE, YELLOW, YELLOW],
            [RED, BLUE, YELLOW, YELLOW],
            [RED, BLUE, YELLOW, YELLOW],
        ]
        self.table_area.start_new_round()

    def bag_state(self) -> Any:
        return json.loads(self.bag.state())["bag"]

    def table_center_state(self) -> Any:
        return json.loads(self.table_area.state())["table center"]

    def factory_state(self, i: int) -> Any:
        return json.loads(self.table_area.state())["factories"][i]

    def state(self) -> Any:
        return json.loads(self.table_area.state())

    def take_from_center(self, tile: str) -> List[Tile]:
        assert len(tile) == 1
        index: int = self.table_center_state().index(tile)
        return self.table_area.take(0, index)

    def test_playing_game_and_refilling_bag_twice(self) -> None:
        self.assertCountEqual(self.table_area.take(1, 1), 4*[RED])
        self.assertCountEqual(self.table_center_state(), "S")
        self.assertCountEqual(self.factory_state(0), "")
        self.assertCountEqual(self.table_area.take(2, 2), 3*[GREEN])
        self.assertCountEqual(self.factory_state(1), "")
        self.assertCountEqual(self.table_center_state(), "SB")
        self.assertCountEqual(self.table_area.take(3, 0), [YELLOW])
        self.assertCountEqual(self.table_center_state(), "SBGGG")
        self.assertCountEqual(self.table_area.take(5, 1), [BLUE])
        self.assertCountEqual(self.table_center_state(), "SBGGGRYY")
        self.assertCountEqual(self.take_from_center('Y'),
                              2*[YELLOW]+[STARTING_PLAYER])
        self.assertCountEqual(self.take_from_center('G'),
                              3*[GREEN])
        self.assertCountEqual(self.table_center_state(), "BR")
        self.table_area.take(4, 0)
        self.table_area.take(6, 3)
        self.table_area.take(7, 3)
        self.table_area.take(0, 0)
        self.assertFalse(self.table_area.is_round_end())
        self.table_area.take(0, 0)
        self.assertTrue(self.table_area.is_round_end())
        self.assertCountEqual(self.bag_state(), "RRRYYYBBBBBB")

        self.used_tiles.give(17*[BLUE])
        self.shuffler.next_take = [
            [BLUE, BLUE, BLUE, BLUE],
            [BLUE, BLUE, YELLOW, YELLOW],
            [RED, RED, RED, YELLOW],
            [BLUE, BLUE, BLUE, BLUE],
            [BLUE, BLUE, BLUE, BLUE],
            [BLUE, BLUE, BLUE, BLUE],
            [BLUE, BLUE, BLUE, BLUE],
        ]
        self.table_area.start_new_round()
        self.table_area.take(1, 0)
        self.table_area.take(2, 0)
        self.table_area.take(3, 0)
        self.table_area.take(4, 0)
        self.table_area.take(5, 0)
        self.table_area.take(6, 0)
        self.table_area.take(7, 0)
        self.assertCountEqual(self.table_center_state(), "SYYY")
        self.assertFalse(self.table_area.is_round_end())
        self.take_from_center("Y")
        self.assertTrue(self.table_area.is_round_end())

        self.assertCountEqual(self.bag_state(), "B")
        self.used_tiles.give(27*[YELLOW])
        self.shuffler.next_take = [
            [BLUE], [YELLOW, YELLOW, YELLOW],  # one factory
            [YELLOW, YELLOW, YELLOW, YELLOW],
            [YELLOW, YELLOW, YELLOW, YELLOW],
            [YELLOW, YELLOW, YELLOW, YELLOW],
            [YELLOW, YELLOW, YELLOW, YELLOW],
            [YELLOW, YELLOW, YELLOW, YELLOW],
            [YELLOW, YELLOW, YELLOW, YELLOW],
        ]


if __name__ == '__main__':
    unittest.main()
