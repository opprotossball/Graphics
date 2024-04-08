import numpy as np
import rotations


p = np.array([0, 0, 1], dtype=float)
axis2 = np.array([1, 0, 0], dtype=float) 
axis = np.array([0, 1, 0], dtype=float) 
angle = 3.1415926536
pp = rotations.axis_angle_rotate(p, axis, angle)
print(pp)
ppp = rotations.axis_angle_rotate(pp, axis2, angle)
print(ppp)
