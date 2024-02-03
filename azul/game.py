from __future__ import annotations
import json
from typing import List, Tuple, Final, Any
from azul.interfaces import (
    GameInterface, StateInterface, TableCenterInterface, BoardInterface,
    NotifyEverybodyInterface)
from azul.simple_types import Tile, FinishRoundResult, STARTING_PLAYER


class Game(GameInterface):
    _bag: StateInterface
    _table_area: TableCenterInterface
    _boards: List[BoardInterface]
    _observable: NotifyEverybodyInterface
    _player_manager: PlayerManager

    class PlayerManager:
        _player_ids: List[int]
        _on_turn: int
        _starting_player_next_round: int
        NO_STARTING_PLAYER: Final = -1

        def __init__(self, player_ids: List[int]):
            self._player_ids = player_ids.copy()
            self._on_turn = 0
            self._starting_player_next_round = Game.PlayerManager.NO_STARTING_PLAYER

        def whos_turn_it_is(self) -> Tuple[int, int]:
            """Returns tuple, player_id, board_index"""
            return (self._player_ids[self._on_turn], self._on_turn)

        def evaluate_tiles_and_move_to_next_player(self, tiles: List[Tile]) -> None:
            if STARTING_PLAYER in tiles:
                assert self._starting_player_next_round == Game.PlayerManager.NO_STARTING_PLAYER
                self._starting_player_next_round = self._on_turn
            self._on_turn = (self._on_turn + 1) % len(self._player_ids)

        def start_new_round(self) -> None:
            assert self._starting_player_next_round != Game.PlayerManager.NO_STARTING_PLAYER
            self._on_turn = self._starting_player_next_round
            self._starting_player_next_round = Game.PlayerManager.NO_STARTING_PLAYER

        @property
        def player_ids(self) -> List[int]:
            return self._player_ids.copy()

    def __init__(self, bag: StateInterface, table_area: TableCenterInterface,
                 player_ids_and_boards: List[Tuple[int, BoardInterface]],
                 observable: NotifyEverybodyInterface):
        self._bag = bag
        self._table_area = table_area
        self._boards = [entry[1] for entry in player_ids_and_boards]
        self._observable = observable
        player_ids = [entry[0] for entry in player_ids_and_boards]
        self._player_manager = Game.PlayerManager(player_ids)

    def _state(self) -> str:
        state: Any = {
            "bag": json.loads(self._bag.state()),
            "table area": json.loads(self._table_area.state()),
            "boads": [json.loads(board.state()) for board in self._boards],
            "players": self._player_manager.player_ids,
            "on turn": self._player_manager.whos_turn_it_is()[1]
        }
        return json.dumps(state)

    def start_game(self) -> None:
        self._table_area.start_new_round()

    def take(self, player_id: int, source_idx: int, idx: int, destination_idx: int) -> bool:
        # check if player_id is on turn
        player_on_turn_id, board_id = self._player_manager.whos_turn_it_is()
        if player_on_turn_id != player_id:
            return False

        taken = self._table_area.take(source_idx, idx)
        if not taken:
            return False
        self._player_manager.evaluate_tiles_and_move_to_next_player(taken)

        self._boards[board_id].put(destination_idx, taken)
        if self._table_area.is_round_end():
            self._table_area.start_new_round()
            self._player_manager.start_new_round()
            finish_round_results = [board.finish_round()
                                    for board in self._boards]
            if FinishRoundResult.GAME_FINISHED in finish_round_results:
                for board in self._boards:
                    board.end_game()
        self._observable.notify_everybody(self._state())
        return True
