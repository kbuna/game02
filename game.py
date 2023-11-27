import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600

AURORA_COLOR1 = (255, 255, 255, 100)
AURORA_COLOR2 = (173, 216, 230, 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aurora Example")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))  # 黒の背景

    for y in range(HEIGHT):
        distance = ((WIDTH // 2) ** 2 + (y - HEIGHT // 2) ** 2) ** 0.5
        normalized_distance = distance / (min(WIDTH, HEIGHT) / 2)
        normalized_distance = min(1.0, normalized_distance)
        alpha = int(normalized_distance * (AURORA_COLOR2[3] - AURORA_COLOR1[3])) + AURORA_COLOR1[3]
        color = AURORA_COLOR1[:3]
        color_with_alpha = color + (alpha,)
        pygame.draw.line(screen, color_with_alpha, (0, y), (WIDTH, y), 1)

    pygame.display.flip()
