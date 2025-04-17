import pygame
import numpy as np
import random

WIDTH, HEIGHT = 800, 800
ARENA_SIZE = 600
ARENA_LEFT = (WIDTH - ARENA_SIZE) // 2
ARENA_TOP = (HEIGHT - ARENA_SIZE) // 2
ARENA_RIGHT = ARENA_LEFT + ARENA_SIZE
ARENA_BOTTOM = ARENA_TOP + ARENA_SIZE

BALL_COLORS = [
    (255, 99, 71), (30, 144, 255), (50, 205, 50), (255, 215, 0),
    (148, 0, 211), (255, 105, 180), (255, 140, 0), (0, 206, 209)
]

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Battle Balls - Viral Simulation')
clock = pygame.time.Clock()

class Ball:
    def __init__(self, idx):
        self.radius = random.randint(18, 28)
        self.pos = np.array([
            random.uniform(ARENA_LEFT + self.radius, ARENA_RIGHT - self.radius),
            random.uniform(ARENA_TOP + self.radius, ARENA_BOTTOM - self.radius)
        ], dtype=np.float64)
        angle = random.uniform(0, 2 * np.pi)
        speed = random.uniform(3, 6)
        self.v = np.array([np.cos(angle) * speed, np.sin(angle) * speed], dtype=np.float64)
        self.color = BALL_COLORS[idx % len(BALL_COLORS)]
        self.energy = 1.0
        self.personality = random.choice(['speedy', 'jumper', 'grower', 'shrinker', 'crazy'])
        self.alive = True
        self.flash = 0

    def update(self):
        if not self.alive:
            return
        # Personnalités
        if self.personality == 'speedy':
            self.v *= 1.01
        elif self.personality == 'jumper' and random.random() < 0.01:
            self.v += np.random.uniform(-4, 4, 2)
        elif self.personality == 'grower':
            self.radius = min(self.radius + 0.01, 50)
        elif self.personality == 'shrinker':
            self.radius = max(self.radius - 0.01, 10)
        elif self.personality == 'crazy' and random.random() < 0.03:
            self.v = np.random.uniform(-6, 6, 2)
        self.pos += self.v
        # Collision avec l'arène
        if self.pos[0] - self.radius < ARENA_LEFT:
            self.pos[0] = ARENA_LEFT + self.radius
            self.v[0] *= -1
        if self.pos[0] + self.radius > ARENA_RIGHT:
            self.pos[0] = ARENA_RIGHT - self.radius
            self.v[0] *= -1
        if self.pos[1] - self.radius < ARENA_TOP:
            self.pos[1] = ARENA_TOP + self.radius
            self.v[1] *= -1
        if self.pos[1] + self.radius > ARENA_BOTTOM:
            self.pos[1] = ARENA_BOTTOM - self.radius
            self.v[1] *= -1
        if self.flash > 0:
            self.flash -= 1

    def draw(self, surface):
        if not self.alive:
            return
        color = (255,255,255) if self.flash > 0 else self.color
        pygame.draw.circle(surface, color, self.pos.astype(int), int(self.radius))
        # Effet d'énergie
        if self.energy > 1.2:
            pygame.draw.circle(surface, (255,255,255), self.pos.astype(int), int(self.radius+6), 2)

balls = [Ball(i) for i in range(8)]

# Effet de fond animé

def draw_background(surface, t):
    for y in range(HEIGHT):
        r = int(30 + 60 * np.sin(2 * np.pi * (y / HEIGHT) + t))
        g = int(30 + 60 * np.sin(2 * np.pi * (y / HEIGHT) + t + 2))
        b = int(30 + 60 * np.sin(2 * np.pi * (y / HEIGHT) + t + 4))
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))

def collide(ball1, ball2):
    if not ball1.alive or not ball2.alive:
        return
    d = np.linalg.norm(ball1.pos - ball2.pos)
    if d < ball1.radius + ball2.radius:
        # Effet visuel
        ball1.flash = ball2.flash = 6
        # La plus grosse absorbe de l'énergie
        if ball1.radius > ball2.radius:
            ball1.energy += 0.1
            ball2.energy -= 0.1
        else:
            ball2.energy += 0.1
            ball1.energy -= 0.1
        # Rebond
        direction = (ball1.pos - ball2.pos) / (d + 1e-6)
        ball1.v += direction * 2
        ball2.v -= direction * 2
        # Si une balle n'a plus d'énergie, elle "explose"
        if ball1.energy < 0.5:
            ball1.alive = False
        if ball2.energy < 0.5:
            ball2.alive = False

def draw_arena(surface, t):
    # Arène qui pulse
    pulse = int(6 + 4 * np.sin(t*2))
    pygame.draw.rect(surface, (255,255,255), (ARENA_LEFT, ARENA_TOP, ARENA_SIZE, ARENA_SIZE), pulse)

def main():
    running = True
    t = 0
    winner = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        t += 0.012
        draw_background(window, t)
        draw_arena(window, t)
        alive_balls = [b for b in balls if b.alive]
        if len(alive_balls) == 1 and not winner:
            winner = alive_balls[0]
        for ball in balls:
            ball.update()
        for i in range(len(balls)):
            for j in range(i+1, len(balls)):
                collide(balls[i], balls[j])
        for ball in balls:
            ball.draw(window)
        # Effet final
        if winner:
            pygame.draw.circle(window, (255,255,255), winner.pos.astype(int), int(winner.radius+20), 6)
            font = pygame.font.SysFont(None, 60)
            text = font.render('Champion!', True, (255,255,255))
            window.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 40))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
