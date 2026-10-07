from enum import Enum


class State(Enum):
    WANDER = 0
    PURSUE = 1,
    FLEE = 2,
    ARRIVE = 3
