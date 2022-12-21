import sys
import pygame
from basegame import BaseGame

WHITE = (255, 255 ,255)
SCREEN = pygame.display.set_mode((600, 600))
CLOCK = pygame.time.Clock()
SCREEN.fill(WHITE)

def two_player():
    run = True
    g = BaseGame(SCREEN, game_size=600, game_pos=(0, 0))
    current_x = True
    while run:
        SCREEN.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if current_x:
                    g.add("x", (y, x))
                    current_x = False
                else:
                    g.add("o", (y, x))
                    current_x = True

                w = g.check_winner()
                if w:
                    run = False
                    print(w, "wins")

        g.draw()
        pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    two_player()

