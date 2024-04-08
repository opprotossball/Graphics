import pygame
from utils import load_scene
from camera import Camera
import time
import numpy as np

pygame.init()
(screen_w, screen_h) = (900, 900)
background = (50, 50, 50)
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('VCam')
clock = pygame.time.Clock()
running = True

scene_path = './data/scene1.csv'

# camera settings
cam_depth = 20.0
camera = Camera(20.0, 20.0, cam_depth)
print(camera)
scene = load_scene(scene_path)

move_speed = 0.01
rotation_speed = 0.001

while (running):

    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background)

    ks = pygame.key.get_pressed()
    # translation
    tr = np.array([0, 0, 0], dtype=float)
    if ks[pygame.K_d]:
        tr[0] += move_speed * dt
    if ks[pygame.K_a]:
        tr[0] -= move_speed * dt
    if ks[pygame.K_UP]:
        tr[1] -= move_speed * dt
    if ks[pygame.K_DOWN]:
        tr[1] += move_speed * dt
    if ks[pygame.K_w]:
        tr[2] += move_speed * dt
    if ks[pygame.K_s]:
        tr[2] -= move_speed * dt
    camera.move(tr)

    # rotation
    angle = rotation_speed * dt
    if ks[pygame.K_1]:
        camera.x_rotation(angle)
    if ks[pygame.K_2]:
        camera.x_rotation(-angle)
    if ks[pygame.K_3]:
        camera.y_rotation(angle)
    if ks[pygame.K_4]:
        camera.y_rotation(-angle)
    if ks[pygame.K_5]:
        camera.z_rotation(angle)
    if ks[pygame.K_6]:
        camera.z_rotation(-angle)

    for edge in camera.shot_scene(scene):        
        a = camera.camera_to_display_space(edge.a, screen_w / 2, screen_h / 2)
        b = camera.camera_to_display_space(edge.b, screen_w / 2, screen_h / 2)
        pygame.draw.line(screen, (255, 0, 0), a, b)
    pygame.display.update()
