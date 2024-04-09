import pygame
from scenes import load_scene
import scenes
from camera import Camera
import numpy as np

# pygame
pygame.init()
(screen_w, screen_h) = (900, 900)
background = (0, 0, 0)
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('VCam')
clock = pygame.time.Clock()
running = True

# create or load scene
# scene_path = './data/scene1.csv'
# scene = load_scene(scene_path)
scene = scenes.cubes((10, 10, 10), 10, 30, 4)

# camera settings
cam_depth = 0.1
move_speed = 0.05
rotation_speed = 1e-3
zoom_speed = 1e-4
camera = Camera(0.1, 0.1, cam_depth)

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

    # zoom
    if ks[pygame.K_EQUALS]:
        camera.zoom(zoom_speed * dt)
    if ks[pygame.K_MINUS]:
        camera.zoom(-zoom_speed * dt)

    for edge in camera.shot_scene(scene):        
        a = camera.camera_to_display_space(edge.a, screen_w / 2, screen_h / 2)
        b = camera.camera_to_display_space(edge.b, screen_w / 2, screen_h / 2)
        pygame.draw.line(screen, (255, 255, 255), a, b)

    pygame.display.update()
