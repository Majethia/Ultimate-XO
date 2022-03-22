import sys
import numpy as np
import pygame

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600

WHITE = (255, 255 ,255)

pygame.init()

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()
SCREEN.fill(WHITE)

grid = pygame.image.load("assets/grid.png")
X = pygame.image.load("assets/X.png")
O = pygame.image.load("assets/o.png")
grid = pygame.transform.scale(grid, (WINDOW_HEIGHT, WINDOW_WIDTH))
X = pygame.transform.scale(X, (WINDOW_HEIGHT/5, WINDOW_WIDTH/5))
O = pygame.transform.scale(O, (WINDOW_HEIGHT/5, WINDOW_WIDTH/5))

class Game:
    def __init__(self) -> None:
        self.grid = np.zeros(shape=(3,3))

    def check_winner(self):
        for n, i in enumerate(self.grid):
            if len(set(i)) == 1 and i[0] != 0:
                grid_to_screen((n, 0), (n, 2))
                return i[0]
        for n, i in enumerate(self.grid.T):
            if len(set(i)) == 1 and i[0] != 0:
                grid_to_screen((0, n), (2, n))
                return i[0]
        d1 = []
        d2 = []
        for i in range(1, 4):
            d1.append(self.grid[i-1][i-1]) 
            d2.append(self.grid[i-1][-i])
        if len(set(d1)) == 1 and d1[0] != 0:
                grid_to_screen((0, 0), (2, 2))
                return d1[0]
        if len(set(d2)) == 1 and d2[0] != 0:
                grid_to_screen((0, 2), (2, 0))
                return d2[0]
        return False

    def draw(self):
        SCREEN.blit(grid, (0, 0))

    def add(self, symbol, pos):
        i, j = pos
        if symbol == "x":
            self.grid[i][j] = 1
            s = X
        else:
            self.grid[i][j] = 2
            s = O
        SCREEN.blit(s, ((WINDOW_HEIGHT/3)*j + WINDOW_HEIGHT/13,(WINDOW_HEIGHT/3)*i + WINDOW_WIDTH/13))

def grid_to_screen(pos1, pos2):
    i1, j1 = pos1
    i2, j2 = pos2
    spos = ((WINDOW_HEIGHT/6) + (WINDOW_HEIGHT/3)*(j1), (WINDOW_WIDTH/6) + (WINDOW_WIDTH/3)*(i1))
    epos = ((WINDOW_HEIGHT/6) + (WINDOW_HEIGHT/3)*(j2), (WINDOW_WIDTH/6) + (WINDOW_WIDTH/3)*(i2))
    pygame.draw.line(
        SCREEN, 
        (0, 0, 0), 
        spos, 
        epos,
        5
        )



def main():
    run = True
    g = Game()
    current_x = True
    while run:
        g.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x, y = pos[0]// (WINDOW_HEIGHT/3), pos[1]// (WINDOW_HEIGHT/3)
                x = int(x)
                y = int(y)
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

        pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()



main()
