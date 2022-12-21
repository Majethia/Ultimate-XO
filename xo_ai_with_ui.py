import sys
import pygame
from basegame import BaseGame

WHITE = (255, 255 ,255)
SCREEN = pygame.display.set_mode((600, 600))
CLOCK = pygame.time.Clock()
SCREEN.fill(WHITE)

def one_player():
    run = True
    g = BaseGame(SCREEN, game_size=600, game_pos=(0, 0))
    # i, j = g.best_move()
    g.grid[0][0] = 2
    while run:
        SCREEN.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                g.add("x", (y, x))
                w = g.check_winner()
                if w:
                    run = False
                    print(w, "wins")
                    break
                g.draw()
                pygame.display.update()

                i, j = g.best_move()
                g.grid[i][j] = 2
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
    one_player()

