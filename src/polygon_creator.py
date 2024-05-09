import numpy as np
from polygon import Polygon

class PolygonCreator:

    def __init__(self, start):
        self.surfaces = []
        self.vertices = [start]
        self.prev = start

    # creates new surface
    def new(self, color=(255, 255, 255)):
        self.surfaces.append(Polygon(self.vertices, color))
        self.vertices = [self.prev]

    # changes prev relative without drawing line
    def go(self, *diff):
        self.prev = self.prev + np.array(list(diff), dtype=float)

    # shot + go
    def add(self, *diff):
        next = self.prev + np.array(list(diff), dtype=float)
        self.vertices.append(next)
        self.prev = next

    # sets absolute position & creates new surface
    def go_to_new(self, *point):
        self.prev = np.array(list(point), dtype=float)
        self.new()
        