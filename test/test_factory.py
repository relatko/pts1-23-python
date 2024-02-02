from __future__ import annotations
import unittest
from typing import List
from test.utils import FakeGiveTiles
from azul.factory import Factory
from azul.interfaces import TakeTilesFromBagInterface
from azul.simple_types import Tile, RED, GREEN


class FakeBag(TakeTilesFromBagInterface):
    next_tiles: List[Tile]

    def take(self, count: int) -> List[Tile]:
        return self.next_tiles


class TestFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.centre: FakeGiveTiles = FakeGiveTiles()
        self.bag: FakeBag = FakeBag()
        self.factory: Factory = Factory(self.bag, self.centre)

    def test_starts_empty(self) -> None:
        self.assertEqual(self.factory.state(), "")
        self.assertTrue(self.factory.is_empty())

    def test_can_take_and_start_new_round(self) -> None:
        self.bag.next_tiles = [RED, RED, GREEN, RED]
        self.factory.start_new_round()
        self.assertFalse(self.factory.is_empty())
        self.assertCountEqual(self.factory.state(), "RRRG")
        self.assertEqual(self.factory.take(3), 3*[RED])
        self.assertCountEqual(self.centre.tiles_given, [GREEN])
        self.assertTrue(self.factory.is_empty())
        self.bag.next_tiles = [GREEN, RED, GREEN, RED]
        self.factory.start_new_round()
        self.assertCountEqual(self.factory.state(), "RRGG")
        self.assertFalse(self.factory.is_empty())

    def test_start_new_round_incorrectly_fails(self) -> None:
        self.bag.next_tiles = [GREEN, RED, GREEN, RED]
        self.factory.start_new_round()
        with self.assertRaises(AssertionError):
            self.factory.start_new_round()

    def test_returns_empty_list_on_error(self) -> None:
        self.assertEqual(self.factory.take(0), [])
        self.bag.next_tiles = [GREEN, RED, GREEN, RED]
        self.factory.start_new_round()
        self.assertEqual(self.factory.take(4), [])

    def test_negative_indices(self) -> None:
        self.assertEqual(self.factory.take(-1), [])
        self.bag.next_tiles = [GREEN, RED, GREEN, RED]
        self.factory.start_new_round()
        self.assertEqual(self.factory.take(-5), [])
        self.assertEqual(self.factory.take(-1), 2*[RED])


if __name__ == '__main__':
    unittest.main()
