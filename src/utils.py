from typing import List
from edge import Edge
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
            a = np.array(coords[:3])
            b = np.array(coords[3:])
            res.append(Edge(a, b))
    return res
