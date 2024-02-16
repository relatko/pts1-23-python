from __future__ import annotations
import json
from typing import List, Tuple
from random import Random
from azul.interfaces import BagUsedTilesInterface, TakeTilesFromBagInterface, StateInterface
from azul.simple_types import Tile, compress_tile_list


class Bag(TakeTilesFromBagInterface, StateInterface):
    _used_tiles: BagUsedTilesInterface
    _tiles: List[Tile]

    class RandomTakeInterface:
        # pylint: disable=unused-argument
        def take(self, count: int, tiles: List[Tile]) -> Tuple[List[Tile], List[Tile]]:
            assert False

    class RandomTake(RandomTakeInterface):
        _random: Random

        def __init__(self, random: Random = Random()):
            self._random = random

        def take(self, count: int, tiles: List[Tile]) -> Tuple[List[Tile], List[Tile]]:
            to_shuffle = tiles.copy()
            self._random.shuffle(to_shuffle)
            return (to_shuffle[0:count], to_shuffle[count:])

    def __init__(self, initial_tiles: List[Tile], used_tiles: BagUsedTilesInterface,
                 random_take: RandomTakeInterface = RandomTake()):
        self._used_tiles = used_tiles
        self._random_take = random_take
        self._tiles = initial_tiles.copy()

    def take(self, count: int) -> List[Tile]:
        if count > len(self._tiles):
            # We want RandomTake to know about each tile taken, helps with tests
            to_return, _ = self._random_take.take(
                len(self._tiles), self._tiles)
            self._tiles = self._used_tiles.take_all()
            count -= len(to_return)
        else:
            to_return = []

        assert count <= len(self._tiles)

        taken, rest = self._random_take.take(count, self._tiles)
        self._tiles = rest
        return to_return + taken

    def state(self) -> str:
        used_tiles_state = json.loads(self._used_tiles.state())
        return json.dumps({"bag": compress_tile_list(self._tiles), "used tiles": used_tiles_state})
