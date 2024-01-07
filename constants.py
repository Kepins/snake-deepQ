from collections import namedtuple
from dataclasses import dataclass
from enum import Enum

Point = namedtuple('Point', ['x', 'y'])


@dataclass
class GameState:
    head: Point
    food: Point
    velocity: Point
    tail: list[Point]


class Action(Enum):
    TURN_LEFT = 0
    GO_STRAIGHT = 1
    TURN_RIGHT = 2


WIDTH, HEIGHT = 5, 5

