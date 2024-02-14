from __future__ import annotations
import unittest
from typing import List
from azul.table_area import TableArea
from azul.interfaces import TileSourceInterface
from azul.simple_types import Tile


class FakeTileSourceFactory:
    ids: List[int]

    def __init__(self) -> None:
        self.ids = []

    def get_tile_source(self, id_: int) -> TileSourceInterface:
        class FakeTileSource(TileSourceInterface):
            is_end: bool
            id_: int
            take_result: List[Tile]
            idx_parameter: int
            factory: FakeTileSourceFactory

            def __init__(self, id_: int, factory: FakeTileSourceFactory) -> None:
                self.id_ = id_
                self.factory = factory

            def take(self, idx: int) -> List[Tile]:
                self.idx_parameter = idx
                return self.take_result

            def is_round_end(self) -> bool:
                return self.is_end

            def start_new_round(self) -> None:
                self.factory.ids.append(self.id_)

            def state(self) -> str:
                return str(self.id_)
        return FakeTileSource(id_, self)


class TestTableArea(unittest.TestCase):
    def setUp(self) -> None:
        self.fake_factory: FakeTileSourceFactory = FakeTileSourceFactory()
        self.factories: List[TileSourceInterface] = [
            self.fake_factory.get_tile_source(i) for i in [1, 3, 2]]
        self.table_center: TileSourceInterface = self.fake_factory.get_tile_source(
            0)
        self.table_area: TableArea = TableArea(
            self.factories, self.table_center)

    def test_new_round_calls_are_in_correct_order(self) -> None:
        self.table_area.start_new_round()
        self.assertTrue(0 in self.fake_factory.ids)
        self.fake_factory.ids.remove(0)
        self.assertEqual(self.fake_factory.ids, [1, 3, 2])


if __name__ == '__main__':
    unittest.main()
