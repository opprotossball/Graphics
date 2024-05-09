from typing import List
from edge import Edge
import numpy as np
import csv
from polygon_creator import PolygonCreator

def surface_cube(sc: PolygonCreator, size):
    sc.add(size, 0, 0)
    sc.add(0, size, 0)
    sc.add(-size, 0, 0)
    sc.new((255, 0, 0))

    sc.add(0, -size, 0)
    sc.add(0, 0, size)
    sc.add(0, size, 0)
    sc.new((0, 255, 0))
    
    sc.add(0, 0, -size)
    sc.add(size, 0, 0)
    sc.add(0, 0, size)
    sc.new((0, 255, 255))

    sc.add(0, 0, -size)
    sc.add(0, -size, 0)
    sc.add(0, 0, size)
    sc.new((0, 0, 255))

def surf():
    sc = PolygonCreator((10, 10, 10))
    surface_cube(sc, 10)
    return sc.surfaces

def surface_cubes(start, size, gap, n):
    sc = PolygonCreator(start)
    sx, sy, sz = start
    for x in range(n):
        for y in range(n):
            for z in range(n):
                surface_cube(sc, size)
                sc.go_to_new(sx + x * (gap + size), sy + y * (gap + size), sz + z * (gap + size))
    surface_cube(sc, size)
