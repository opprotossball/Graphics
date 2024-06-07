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

    sc.add(0, 0, -size)
    sc.add(-size, 0, 0)
    sc.add(0, 0, size)
    sc.new((255, 255, 0))

    sc.add(0, size, 0)
    sc.add(size, 0, 0)
    sc.add(0, -size, 0)
    sc.new((255, 0, 255))

def offset_cubes(start, size, x_gap, y_gap, z_gap, n):
    sc = PolygonCreator(start)
    sx, sy, sz = start
    for x in range(n):
        for y in range(n):
            for z in range(n):
                surface_cube(sc, size)
                sc.go_to_new(sx + x * (x_gap + size), sy + y * (y_gap + size), sz + z * (z_gap + size))
    surface_cube(sc, size)
    return sc.surfaces

def cubes(start, size, gap, n):
    return offset_cubes(start, size, gap, gap, gap, n)

def cube_line(start, size, x_gap, y_gap, z_gap, n):
    sc = PolygonCreator(start)
    sx, sy, sz = start
    for i in range(n+1):
        surface_cube(sc, size)
        sc.go_to_new(sx + i * (x_gap + size), sy + i * (y_gap + size), sz + i * (z_gap + size))
    return sc.surfaces
