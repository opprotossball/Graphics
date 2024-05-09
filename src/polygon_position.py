from enum import Enum

class PolygonPosition(Enum):
    ON_PLANE = 0,
    IN_FRONT = 1,
    BEHIND = 2,
    INTERSECTS = 3
