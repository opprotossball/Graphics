from edge import Edge
import numpy as np

class Path:

    def __init__(self, start):
        self.edges = []
        self.prev = start

    # changes prev relative without drawing line
    def go(self, *diff):
        self.prev = self.prev + np.array(list(diff), dtype=float)

    # draws line without changing prev
    def shot(self, *diff):
        next = self.prev + np.array(list(diff), dtype=float)
        self.edges.append(Edge(self.prev, next))

    # shot + go
    def add(self, *diff):
        next = self.prev + np.array(list(diff), dtype=float)
        self.edges.append(Edge(self.prev, next))
        self.prev = next

    # sets absolute position
    def goto(self, *point):
        self.prev = np.array(list(point), dtype=float)
