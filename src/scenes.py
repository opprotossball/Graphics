from typing import List
from edge import Edge
import numpy as np
import csv
from path import Path

def load_scene(path: str) -> list[Edge]:
    res = []
    with open(path, mode='r') as f:
        rd = csv.reader(f)
        for l in rd:
            if len(l) != 6:
                raise ValueError(f'{path}: incorrect file content')
            coords = [float(v) for v in l]
            a = np.array(coords[:3])
            b = np.array(coords[3:])
            res.append(Edge(a, b))
    return res

def cube(p, size) -> Path:
    # bottom
    p.add(size, 0, 0)
    p.add(0, size, 0)
    p.add(-size, 0, 0)
    p.add(0, -size, 0)
    # top
    p.add(0, 0, size)
    p.add(size, 0, 0)
    p.shot(0, 0, -size)
    p.add(0, size, 0)
    p.shot(0, 0, -size)
    p.add(-size, 0, 0)
    p.shot(0, 0, -size)
    p.add(0, -size, 0)

def cubes(start, size, gap, n) -> list[Edge]:
    p = Path(start)
    sx, sy, sz = start
    for x in range(n):
        for y in range(n):
            for z in range(n):
                cube(p, size)
                p.goto(sx + x * (gap + size), sy + y * (gap + size), sz + z * (gap + size))
    cube(p, size)
    return p.edges
    