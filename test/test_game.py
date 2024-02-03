from __future__ import annotations
import unittest
from azul.simple_types import STARTING_PLAYER, RED
from azul.game import Game


class TestGamePlayerManager(unittest.TestCase):
    def setUp(self) -> None:
        self.player_manager = Game.PlayerManager([25, 34, 11])

    def test_switching_turns(self) -> None:
        self.assertEqual(self.player_manager.whos_turn_it_is(), (25, 0))
        self.player_manager.evaluate_tiles_and_move_to_next_player([])
        self.assertEqual(self.player_manager.whos_turn_it_is(), (34, 1))
        self.player_manager.evaluate_tiles_and_move_to_next_player([])
        self.assertEqual(self.player_manager.whos_turn_it_is(), (11, 2))
        self.player_manager.evaluate_tiles_and_move_to_next_player([])
        self.assertEqual(self.player_manager.whos_turn_it_is(), (25, 0))

    def test_set_starting_player_and_new_turn(self) -> None:
        self.player_manager.evaluate_tiles_and_move_to_next_player([])
        self.player_manager.evaluate_tiles_and_move_to_next_player(
            [RED, STARTING_PLAYER, RED])
        self.player_manager.evaluate_tiles_and_move_to_next_player([])
        self.player_manager.evaluate_tiles_and_move_to_next_player([RED])
        self.player_manager.start_new_round()
        self.assertEqual(self.player_manager.whos_turn_it_is(), (34, 1))
        self.player_manager.evaluate_tiles_and_move_to_next_player([])
        self.assertEqual(self.player_manager.whos_turn_it_is(), (11, 2))

    def test_no_starting_player_throws(self) -> None:
        self.player_manager.evaluate_tiles_and_move_to_next_player([RED])
        with self.assertRaises(AssertionError):
            self.player_manager.start_new_round()

    def test_two_starting_player_tiles_throw_throws(self) -> None:
        self.player_manager.evaluate_tiles_and_move_to_next_player([
            STARTING_PLAYER])
        with self.assertRaises(AssertionError):
            self.player_manager.evaluate_tiles_and_move_to_next_player([
                STARTING_PLAYER])


if __name__ == '__main__':
    unittest.main()
