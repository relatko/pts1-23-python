from __future__ import annotations
import unittest
import json
from typing import Any, List
from test.utils import FakeShuffler
from azul.simple_types import RED, BLUE, YELLOW
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

        self.shuffler.next_take = [
            [RED, RED, RED, RED],
            [RED, RED, RED, RED],
            [RED, RED, RED, RED],
            [BLUE, BLUE, BLUE, BLUE],
            [BLUE, BLUE, BLUE, YELLOW],
        ]

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

    def get_points(self, i: int) -> Any:
        return json.loads(self.observer.messages[-1])["boards"][i-1]["points"]

    def take_from_center(self, player: int, tile: str, destination_index: int) -> bool:
        assert len(tile) == 1
        index: int = self.table_center_state().index(tile)
        return self.game.take(player, 0, index, destination_index)

    def test_play(self) -> None:
        self.game.start_game()
        self.assertCountEqual(self.table_center_state(), "S")
        self.assertCountEqual(self.factory_state(1), "RRRR")
        self.assertTrue(self.game.take(9, 1, 1, 1))
        self.assertCountEqual(self.patternline_state(1, 1), "R")
        self.assertCountEqual(self.floor_state(1), "RRR")

        self.assertFalse(self.game.take(9, 2, 1, 1))   # not on turn

        self.assertTrue(self.game.take(7, 5, 0, 3))
        self.assertTrue(self.game.take(9, 3, 0, 1))    # drops
        self.assertTrue(self.game.take(7, 4, 0, 4))
        self.assertTrue(self.game.take(9, 2, 0, 1))    # drops

        # next .take call will finish turn
        self.shuffler.next_take = [
            [RED, RED, RED, RED],
            [RED, RED, RED, RED],
            [BLUE, BLUE, BLUE, BLUE],
            [BLUE, BLUE, BLUE, BLUE],
            [BLUE, BLUE, BLUE, BLUE],
        ]
        self.assertTrue(self.take_from_center(7, "Y", 1))

        self.assertEqual(self.get_points(1), 0)
        self.assertEqual(self.get_points(2), 2)

        # drops as we already have BLUE on wallline 4
        self.assertTrue(self.game.take(7, 5, 1, 4))
        self.assertCountEqual(self.floor_state(2), "BBBB")


if __name__ == '__main__':
    unittest.main()
