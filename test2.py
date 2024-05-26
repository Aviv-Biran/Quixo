import pygame
import pygame.freetype  # Import the freetype module.
from Constants import *


pygame.init()
screen = pygame.display.set_mode((800, 600))
GAME_FONT = pygame.freetype.SysFont('Comic Sans MS', 24)
running =  True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255,255,255))
    # You can use `render` and then blit the text surface ...
    text_surface, rect = GAME_FONT.render("Hello World!", (0, 0, 0))
    screen.blit(text_surface, (WIDTH // 2, HEIGHT // 2))
    # or just `render_to` the target surface.
    GAME_FONT.render_to(screen, (40, 350), "Hello World!", (0, 0, 0))

    pygame.display.flip()