from __future__ import annotations
from typing import List, Tuple, Optional
from azul.bag import Bag
from azul.used_tiles import UsedTiles
from azul.factory import Factory
from azul.table_center import TableCenter
from azul.table_area import TableArea
from azul.board import Board
from azul.floor import Floor
from azul.wall_line import WallLine
from azul.pattern_line import PatternLine
from azul.game_finished import GameFinished
from azul.game import Game
from azul.game_observable import GameObservable
from azul.final_points_calculation import FinalPointsCalculation
from azul.interfaces import (TableAreaInterface, StateInterface, GameInterface,
                             TileSourceInterface, BoardInterface, PatternLineInterface,
                             GiveTilesInterface)
from azul.simple_types import Tile, RED, GREEN, BLACK, BLUE, YELLOW, Points

GAME_TILES: Tuple[Tile, ...] = 20*(RED, GREEN, BLUE, BLACK, YELLOW)


def create_table_area(number_of_players: int, random_take: Bag.RandomTakeInterface,
                      tile_list: Tuple[Tile, ...] = GAME_TILES) -> \
        Tuple[TableAreaInterface, StateInterface, GiveTilesInterface]:
    """ Returns TableArea, Bag, UsedTiles."""
    used_tiles: UsedTiles = UsedTiles()
    bag = Bag(list(tile_list), used_tiles, random_take)
    table_center = TableCenter()
    number_of_factories = {2: 5, 3: 7, 5: 9}[number_of_players]
    factories: List[TileSourceInterface] = [
        Factory(bag, table_center) for _ in range(number_of_factories)]
    table_area: TableAreaInterface = TableArea(factories, table_center)
    return (table_area, bag, used_tiles)


WALL_TILE_PATTERN: Tuple[Tuple[Tile, ...], ...] = tuple(tuple((BLUE, YELLOW, RED, BLACK, GREEN)[i+j]
                                                              for i in range(4)) for j in range(4))
no_tile: Optional[Tile] = None    # mypy can be a bit stupit with List types
WALL_STARTING_TILES: Tuple[Tuple[Optional[Tile], ...], ...] = 5*(5*(no_tile,),)
FLOOR_POINT_PATTERN: Tuple[Points, ...] = tuple(
    Points(x) for x in 2*[-1]+3*[-2]+2*[-3])


def create_board(used_tiles: GiveTilesInterface,
                 wall_starting_tiles: Tuple[Tuple[Optional[Tile], ...], ...]
                 = WALL_STARTING_TILES) -> Board:
    floor = Floor(list(FLOOR_POINT_PATTERN), used_tiles)
    wall_lines: List[WallLine] = [
        WallLine(list(WALL_TILE_PATTERN[i]), list(wall_starting_tiles[i])) for i in range(5)]
    for i in range(4):
        wall_lines[i].line_down = wall_lines[i+1]
        wall_lines[i+1].line_up = wall_lines[i]
    capacities = [1, 2, 3, 4, 5]
    pattern_lines: List[PatternLineInterface] = [
        PatternLine(capacities[i], floor, used_tiles, wall_lines[i]) for i in range(4)]
    return Board(GameFinished(), FinalPointsCalculation(), pattern_lines, list(*wall_lines), floor)


def create_game(players: List[int], random_take: Bag.RandomTakeInterface) -> GameInterface:
    table_area, bag, used_tiles = create_table_area(len(players), random_take)
    boards: List[Tuple[int, BoardInterface]] = [
        (index, create_board(used_tiles)) for index in players]
    observable = GameObservable()
    return Game(bag, table_area, boards, observable)
