import pygame
import scenes
from camera import Camera
from polygon import Polygon
import numpy as np

tstsc = scenes.surf()

# pygame
pygame.init()
(screen_w, screen_h) = (900, 900)
background = (0, 0, 0)
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('VCam')
clock = pygame.time.Clock()
running = True

# camera settings
cam_depth = 0.1
move_speed = 0.05
rotation_speed = 1e-3
zoom_speed = 1e-4
camera = Camera(tstsc, 0.1, 0.1, cam_depth)

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
        camera.rotate_x(angle)
    if ks[pygame.K_2]:
        camera.rotate_x(-angle)
    if ks[pygame.K_3]:
        camera.rotate_y(-angle)
    if ks[pygame.K_4]:
        camera.rotate_y(angle)
    if ks[pygame.K_5]:
        camera.rotate_z(angle)
    if ks[pygame.K_6]:
        camera.rotate_z(-angle)

    if ks[pygame.K_SPACE]:
        camera.tst()

    # zoom
    if ks[pygame.K_EQUALS]:
        camera.zoom(zoom_speed * dt)
    if ks[pygame.K_MINUS]:
        camera.zoom(-zoom_speed * dt)

    srfcs = camera.shot_scene()
    for s in srfcs:
        vertices = [camera.camera_to_display_space(p, screen_w / 2, screen_h / 2) for p in s.vertices]
        pygame.draw.polygon(screen, s.color, vertices)

    pygame.display.update()
