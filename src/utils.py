from typing import List
from edge import Edge
from vector import Vector
import numpy as np
import csv

def load_scene(path: str) -> list[Edge]:
    res = []
    with open(path, mode='r') as f:
        rd = csv.reader(f)
        for l in rd:
            if len(l) != 6:
                raise ValueError(f'{path}: incorrect file content')
            coords = [float(v) for v in l]
            a = Vector(coords[0], coords[1], coords[2])
            b = Vector(coords[3], coords[4], coords[5])
            res.append(Edge(a, b))
    return res

def dot(a: Vector, b: Vector) -> float:
    return np.dot(a.pos, b.pos)
