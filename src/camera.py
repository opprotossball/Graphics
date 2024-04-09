from edge import Edge
import numpy as np
from quaternion import Quaternion
import rotations

class Camera:

    def __init__(self, half_width: float, half_height: float, depth: float, min_depth=1e-5, max_depth=1e5):
        self.half_width = half_width
        self.half_height = half_height
        self._view_center = np.array([0, 0, 0], dtype=float)
        self._depth = depth
        self._min_depth = min_depth
        self._max_depth = max_depth
        self._rotation = Quaternion()

    # find intersection with viewing plane in camera space
    def plane_intersection(self, point):
        t = self._depth / point[2]
        return t * point

    def move(self, translation):
        self._view_center += self.x_axis() * translation[0] + self.y_axis() * translation[1] + self.z_axis() * translation[2]
    
    def rotate_x(self, angle):
        self._rotation *= rotations.axis_angle_to_quat(np.array([1, 0, 0], dtype=float), angle)

    def rotate_y(self, angle):
        self._rotation *= rotations.axis_angle_to_quat(np.array([0, 1, 0], dtype=float), angle)

    def rotate_z(self, angle):
        self._rotation *= rotations.axis_angle_to_quat(np.array([0, 0, 1], dtype=float), angle)

    def x_axis(self):
        return rotations.quat_rotate(np.array([1, 0, 0], dtype=float), self._rotation)
    
    def y_axis(self):
        return rotations.quat_rotate(np.array([0, 1, 0], dtype=float), self._rotation)
    
    def z_axis(self):
        return rotations.quat_rotate(np.array([0, 0, 1], dtype=float), self._rotation)

    def zoom(self, delta):
        self._depth += delta
        self._depth = min(self._depth, self._max_depth)
        self._depth = max(self._depth, self._min_depth)

    def scene_to_camera_space(self, point):
        diff = point - self._view_center
        axes = np.array([self.x_axis(), self.y_axis(), self.z_axis()])
        return diff @ axes.T
    
    def edge_to_camera_space(self, edge: Edge):
        a = self.scene_to_camera_space(edge.a)
        b = self.scene_to_camera_space(edge.b)
        # check if both ends are on the correct side of plane (a.z >= 0 && b.z >= 0) 
        # if a[2] <= 0 or b[2] <= 0:
        if a[2] <= self._depth or b[2] <= self._depth:
            return None
        ai = self.plane_intersection(a)
        # check if points fit in frame
        # if abs(ai[0]) > self.half_width or abs(ai[1]) > self.half_height:
        #     return None 
        bi = self.plane_intersection(b)
        # if abs(bi[0]) > self.half_width or abs(bi[1]) > self.half_height:
        #     return None
        clipped = self.clip(Edge(ai, bi))
        return clipped
    
    def shot_scene(self, scene: list[Edge]) -> list[Edge]:
        res = []
        for edge in scene:
            edge_in_camera = self.edge_to_camera_space(edge)
            if edge_in_camera is not None:
                res.append(edge_in_camera)
        return res

    def in_view(self, point) -> bool:
        return abs(point[0]) < self.half_width and abs(point[1]) < self.half_height

    def clip_bottom(self, x1, y1, x2, y2):
        if y1 > -self.half_height:
            return None
        dx = x2 - x1
        dy = y2 - y1
        t = (self.half_height - y1) / dy
        x = x1 + t * dx
        if abs(x) < self.half_width:
            print('bottom')
            return x, self.half_height
        return None
    
    def clip_top(self, x1, y1, x2, y2):
        if y1 < self.half_height:
            return None
        dx = x2 - x1
        dy = y2 - y1
        t = (-self.half_height - y1) / dy
        x = x1 + t * dx
        if abs(x) < self.half_width:
            print('top')
            return x, -self.half_height
        return None
    
    def clip_right(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        t = (self.half_width - x1) / dx
        y = y1 + t * dy
        if (abs(y) < self.half_height):
            print('right')
            return self.half_width, y
        return None
    
    def clip_left(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        t = (-self.half_width - x1) / dx
        y = y1 + t * dy
        if (abs(y) < self.half_height):
            print('left')
            return -self.half_width, y
        return None

    def clip(self, edge: Edge) -> Edge:
        res = Edge(edge.a, edge.b)
        x1 = edge.a[0]
        y1 = edge.a[1]
        x2 = edge.b[0]
        y2 = edge.b[1]
        clips = [self.clip_bottom, self.clip_top, self.clip_right, self.clip_left]
        # point b
        if not self.in_view(edge.b):
            clipped = None
            for c in clips:
                clipped = c(x1, y1, x2, y2)
                if clipped is not None:
                    break
            else:
                return None
            res.b[0], res.b[1] = clipped
        # point a
        if not self.in_view(edge.a):
            clipped = None
            for c in clips:
                clipped = c(x2, y2, x1, y1)
                if clipped is not None:
                    break
            else:
                return None
            res.a[0], res.a[1] = clipped
        return res

    def camera_to_display_space(self, point, display_half_width, display_half_height):
        x = point[0] * display_half_width / self.half_width + display_half_width
        y = point[1] * display_half_height / self.half_height + display_half_height
        return x, y
