import pygame
import numpy as np
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Ball:
    def __init__(self, position, velocity, radius=10):
        self.pos = np.array(position, dtype=np.float64)
        self.v = np.array(velocity, dtype=np.float64)
        self.radius = radius
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 800
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Balle rebondissant dans un carré')
    clock = pygame.time.Clock()

    # Dégradé de fond dynamique
    def draw_gradient(surface, t):
        for y in range(HEIGHT):
            # Animation du dégradé avec t
            r = int(40 + 80 * np.sin(2 * np.pi * (y / HEIGHT) + t))
            g = int(40 + 80 * np.sin(2 * np.pi * (y / HEIGHT) + t + 2))
            b = int(40 + 80 * np.sin(2 * np.pi * (y / HEIGHT) + t + 4))
            # Clamp les valeurs pour éviter l'erreur
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))

    # Définir les bords du carré (centré)
    SQUARE_SIZE = 600
    SQUARE_LEFT = (WIDTH - SQUARE_SIZE) // 2
    SQUARE_TOP = (HEIGHT - SQUARE_SIZE) // 2
    SQUARE_RIGHT = SQUARE_LEFT + SQUARE_SIZE
    SQUARE_BOTTOM = SQUARE_TOP + SQUARE_SIZE

    # Initialisation de la balle
    ball = Ball(position=[WIDTH/2, HEIGHT/2], velocity=[4, 3], radius=15)
    GRAVITY = 0.15
    running = True
    t = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Mise à jour de la position de la balle
        ball.v[1] += GRAVITY
        ball.pos += ball.v

        # Collision avec les bords du carré
        if ball.pos[0] - ball.radius < SQUARE_LEFT:
            ball.pos[0] = SQUARE_LEFT + ball.radius
            ball.v[0] *= -1
        if ball.pos[0] + ball.radius > SQUARE_RIGHT:
            ball.pos[0] = SQUARE_RIGHT - ball.radius
            ball.v[0] *= -1
        if ball.pos[1] - ball.radius < SQUARE_TOP:
            ball.pos[1] = SQUARE_TOP + ball.radius
            ball.v[1] *= -1
        if ball.pos[1] + ball.radius > SQUARE_BOTTOM:
            ball.pos[1] = SQUARE_BOTTOM - ball.radius
            ball.v[1] *= -1

        # Dessiner le fond animé
        draw_gradient(window, t)
        t += 0.01
        # Dessiner le carré
        pygame.draw.rect(window, WHITE, (SQUARE_LEFT, SQUARE_TOP, SQUARE_SIZE, SQUARE_SIZE), 3)
        # Dessiner la balle
        pygame.draw.circle(window, ball.color, ball.pos.astype(int), ball.radius)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
