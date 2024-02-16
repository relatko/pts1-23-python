from __future__ import annotations
import unittest
import json
from typing import Any, List, Tuple
from test.utils import FakeShuffler
from azul.interfaces import ObserverInterface
from azul.factories import create_game


class FakeObserver(ObserverInterface):
    messages: List[str]

    def __init__(self) -> None:
        self.messages: List[str] = []

    def notify(self, new_state: str) -> None:
        self.messages.append(new_state)


class TestGame(unittest.TestCase):
    def setUp(self) -> None:
        self.shuffler: FakeShuffler = FakeShuffler()
        self.game, self.observable = create_game([9, 7], self.shuffler)
        self.observer = FakeObserver()
        self.observable.register_observer(self.observer)

    def bag_state(self) -> Any:
        return json.loads(self.observer.messages[-1])["bag"]["bag"]

    def table_center_state(self) -> Any:
        return json.loads(self.observer.messages[-1])["table area"]["table center"]

    def factory_state(self, i: int) -> Any:
        return json.loads(self.observer.messages[-1])["table area"]["factories"][i-1]

    def patternline_state(self, i: int, j: int) -> Any:
        return json.loads(self.observer.messages[-1])["boards"][i-1]["pattern lines"][j-1]["tiles"]

    def floor_state(self, i: int) -> Any:
        return json.loads(self.observer.messages[-1])["boards"][i-1]["floor"]

    def used_tiles_state(self) -> Any:
        return json.loads(self.observer.messages[-1])["bag"]["used tiles"]

    def get_points(self, i: int) -> Any:
        return json.loads(self.observer.messages[-1])["boards"][i-1]["points"]

    def take_from_factories(self, instructions: List[Tuple[int, int, int, int]]) -> None:
        for player, source, index, line in instructions:
            self.assertTrue(self.game.take(player, source, index, line))

    def take_from_center(self, player: int, tile: str, destination_index: int) -> bool:
        assert len(tile) == 1
        index: int = self.table_center_state().index(tile)
        return self.game.take(player, 0, index, destination_index)

    def test_play(self) -> None:
        self.shuffler.instructions(["RRRR", "RRRR", "RRRR", "BBBB", "BBBY"])
        self.game.start_game()
        self.assertCountEqual(self.table_center_state(), "S")
        self.assertCountEqual(self.factory_state(1), "RRRR")
        self.assertTrue(self.game.take(9, 1, 1, 1))
        self.assertCountEqual(self.patternline_state(1, 1), "R")
        self.assertCountEqual(self.floor_state(1), "RRR")
        self.assertFalse(self.game.take(9, 2, 1, 1))   # not on turn
        self.take_from_factories(
            [(7, 5, 0, 3), (9, 3, 0, 1), (7, 4, 0, 4), (9, 2, 0, 1)])
        self.shuffler.instructions(["RRRR", "RRRR", "BBBB", "BBBB", "BBBB"])
        self.assertTrue(self.take_from_center(7, "Y", 1))
        # turn end
        self.assertEqual(self.get_points(1), 0)
        self.assertEqual(self.get_points(2), 2)
        self.assertCountEqual(self.used_tiles_state(), "RRRBBRRRRBBBRRRR")

        self.assertTrue(self.game.take(7, 5, 1, 4))
        self.assertCountEqual(self.floor_state(2), "BBBB")
        self.take_from_factories(
            [(9, 4, 0, 4), (7, 1, 0, 4), (9, 2, 0, 4), (7, 3, 0, 5)])
        self.shuffler.instructions(["BYYY", "YYYY", "YYYY", "YYYY", "YYYY"])
        self.game.take(9, 0, 0, 1)
        # turn end

        self.take_from_factories([(9, 1, 1, 3), (7, 2, 0, 4), (9, 3, 0, 4), (7, 4, 0, 4),
                                  (9, 5, 0, 4)])
        self.shuffler.instructions(["GGGG", "GGGG", "GGGG", "GGGG", "GGGG"])
        self.take_from_center(7, "B", 1)
        # turn end

        self.take_from_factories([(7, 1, 0, 4), (9, 2, 0, 4), (7, 3, 0, 3), (9, 4, 0, 5),
                                  (7, 5, 0, 2)])
        self.shuffler.instructions(["LLLL", "LLLL", "LLLL", "LLLL", "LLLL"])
        self.game.take(9, 0, 0, 2)
        # turn end

        self.take_from_factories([(9, 2, 0, 4), (7, 3, 0, 2), (9, 4, 0, 5), (7, 5, 0, 3),
                                  (9, 1, 0, 4)])
        # test if BLACK tiles are returned in time for the refill
        self.shuffler.instructions(["LLLL", "LLLL", "GGGG", "GGGG", "YYYY"])
        self.assertTrue(self.game.take(7, 0, 0, 2))
        # turn end, refill bag

        self.take_from_factories([(7, 1, 0, 4), (9, 2, 0, 4), (7, 3, 0, 3), (9, 4, 0, 5),
                                  (7, 5, 0, 1)])
        self.assertFalse(json.loads(self.observer.messages[-1])["finished"])
        self.assertTrue(self.game.take(9, 0, 0, 2))
        # turn end, game finished
        self.assertTrue(json.loads(self.observer.messages[-1])["finished"])
        self.assertFalse(self.game.take(9, 0, 0, 1))


if __name__ == '__main__':
    unittest.main()
