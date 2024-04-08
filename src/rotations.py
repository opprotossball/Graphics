from quaternion import Quaternion
from math import sin, cos
import numpy as np

def axis_angle_to_quat(axis, angle) -> Quaternion:
    a = cos(angle / 2)
    im = sin(angle / 2)
    return Quaternion(a, im * axis[0], im * axis[1], im * axis[2])

def quat_rotate(point, quat):
    p = Quaternion(0.0, point[0], point[1], point[2])
    pr =  quat * p * quat.inversed()
    return pr.as_vec()[1:]

def axis_angle_rotate(point, axis, angle):
    quat = axis_angle_to_quat(axis, angle)
    return quat_rotate(point, quat)
