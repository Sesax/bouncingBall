import pygame
import numpy as np
import math
import random

BLACK = (0, 0, 0)

class Ball:
    def __init__(self, position, velocity):
        self.pos = np.array(position, dtype=np.float64)
        self.v = np.array(velocity, dtype=np.float64)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.is_in = True

def draw_arc(window, center, radius, start_angle, end_angle, color):
    p1 = center + (radius + 1000) * np.array([math.cos(start_angle), math.sin(start_angle)])
    p2 = center + (radius + 1000) * np.array([math.cos(end_angle), math.sin(end_angle)])
    pygame.draw.polygon(window, color, [center, p1, p2], 0)

def is_ball_in_arc(ball_pos, circle_center, start_angle, end_angle):
    dx = ball_pos[0] - circle_center[0]
    dy = ball_pos[1] - circle_center[1]
    ball_angle = math.atan2(dy, dx)
    end_angle = end_angle % (2 * math.pi)
    start_angle = start_angle % (2 * math.pi)
    if start_angle > end_angle:
        end_angle += 2 * math.pi
    if (start_angle <= ball_angle <= end_angle) or (start_angle <= ball_angle + 2 * math.pi <= end_angle):
        return True

pygame.init()
WIDTH = 800
HEIGHT = 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

CIRCLE_CENTER = np.array([WIDTH / 2, HEIGHT / 2], dtype=np.float64)
BALL_RADIUS = 5
ball_pos = np.array([WIDTH / 2, HEIGHT / 2 - 120], dtype=np.float64)
running = True
GRAVITY = 0.2
spinning_speed = 0.01
ball_vel = np.array([0, 0], dtype=np.float64)
ball = Ball(ball_pos, ball_vel)

# Liste des cercles avec (rayon, angle de départ, angle de fin, couleur de l'arc)
circles = [
    {"radius": 150, "start_angle": math.radians(-30), "end_angle": math.radians(30), "color": (255, 165, 0)},  # Orange
    {"radius": 200, "start_angle": math.radians(60), "end_angle": math.radians(120), "color": (255, 0, 0)},  # Rouge
    {"radius": 250, "start_angle": math.radians(150), "end_angle": math.radians(210), "color": (0, 255, 0)}  # Vert
]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Rotation des arcs
    for circle in circles:
        circle["start_angle"] += spinning_speed
        circle["end_angle"] += spinning_speed

    # Mise à jour de la position de la balle
    ball.v[1] += GRAVITY
    ball.pos += ball.v

    # Détection de collision avec les bords de l'écran
    if ball.pos[1] > HEIGHT or ball.pos[0] < 0 or ball.pos[0] > WIDTH or ball.pos[1] < 0:
        ball.pos = np.array([WIDTH / 2, HEIGHT / 2 - 120], dtype=np.float64)
        ball.v = np.array([random.uniform(-4, 4), random.uniform(-1, 1)], dtype=np.float64)

    # Collision avec les cercles
    for circle in circles:
        dist = np.linalg.norm(ball.pos - CIRCLE_CENTER)
        if dist + BALL_RADIUS > circle["radius"]:
            if is_ball_in_arc(ball.pos, CIRCLE_CENTER, circle["start_angle"], circle["end_angle"]):
                ball.is_in = False
            if ball.is_in:
                d = ball.pos - CIRCLE_CENTER
                d_unit = d / np.linalg.norm(d)
                ball.pos = CIRCLE_CENTER + (circle["radius"] - BALL_RADIUS) * d_unit
                t = np.array([-d[1], d[0]], dtype=np.float64)
                proj_v_t = (np.dot(ball.v, t) / np.dot(t, t)) * t
                ball.v = 2 * proj_v_t - ball.v
                ball.v += t * spinning_speed
            ball.is_in = True

    # Dessiner l'arrière-plan
    window.fill(BLACK)

    # Dessiner les cercles et leurs arcs respectifs
    for circle in circles:
        pygame.draw.circle(window, circle["color"], CIRCLE_CENTER.astype(int), circle["radius"], 3)
        draw_arc(window, CIRCLE_CENTER, circle["radius"], circle["start_angle"], circle["end_angle"], circle["color"])

    # Dessiner la balle
    pygame.draw.circle(window, ball.color, ball.pos.astype(int), BALL_RADIUS)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
