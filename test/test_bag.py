from __future__ import annotations
import unittest
import json
from typing import List, Any
from test.utils import FakeShuffler
from azul.bag import Bag
from azul.interfaces import BagUsedTilesInterface
from azul.simple_types import Tile, RED, GREEN


class FakeUsedTiles(BagUsedTilesInterface):
    to_take: List[Tile]

    def take_all(self) -> List[Tile]:
        return self.to_take

    def state(self) -> str:
        return json.dumps("UT")


class TestBag(unittest.TestCase):
    def setUp(self) -> None:
        self.shuffler: FakeShuffler = FakeShuffler()
        self.used_tiles: FakeUsedTiles = FakeUsedTiles()
        tiles = 2*[RED, GREEN]
        self.bag: Bag = Bag(tiles, self.used_tiles, self.shuffler)
        self.endpoint1 = self.bag.get_endpoint("1")
        self.endpoint2 = self.bag.get_endpoint("2")

    def state(self) -> Any:
        return json.loads(self.bag.state())

    @unittest.skip("For now")
    def test_we_can_take_tiles_from_bag_with_remainder(self) -> None:
        self.shuffler.next_take = {
            "1": [RED],
            "2": [RED, GREEN, GREEN],
        }
        self.assertCountEqual(self.endpoint1.take(1), [RED])
        self.assertCountEqual(self.state()["bag"], "RGG")
        self.assertCountEqual(self.endpoint2.take(3), [RED, GREEN, GREEN])
        self.assertCountEqual(self.state()["bag"], "")
        self.shuffler.next_take = {
            "1": [RED],
        }
        self.used_tiles.to_take = [RED, RED]
        self.assertCountEqual(self.endpoint1.take(1), [RED])
        self.assertCountEqual(self.state()["bag"], "R")

    def test_we_can_take_tiles_from_bag_no_remainder(self) -> None:
        self.shuffler.next_take = {
            # +2*[RED, GREEN] in the remaining of the bag before refill
            "1": [GREEN],
        }
        self.used_tiles.to_take = [RED, GREEN]
        self.assertCountEqual(self.endpoint1.take(5), 2*[RED, GREEN]+[GREEN])
        self.assertCountEqual(self.state()["bag"], "R")

    def test_state(self) -> None:
        self.assertCountEqual(self.state()["bag"], "RRGG")
        self.assertEqual(self.state()["used tiles"], "UT")


if __name__ == '__main__':
    unittest.main()
