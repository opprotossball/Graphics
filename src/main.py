import pygame
from utils import load_scene
from vector import Vector
from camera import Camera

pygame.init()
(screen_w, screen_h) = (900, 600)
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('VCam')
running = True

scene_path = './data/scene1.csv'

# camera settings
cam_coords = Vector(20.0, 0, 0)
cam_depth = 10.0
n = Vector(-1.0, 0, 0)
camera = Camera(100.0, 100.0, cam_depth, cam_coords, n)
print(camera)
scene = load_scene(scene_path)

# while (running):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

for e in scene:
    print(e)

print('------------------')

shot = camera.shot_scene(scene)
for e in shot:
    print(e)
