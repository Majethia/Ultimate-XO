import numpy as np
import pygame
import sys

WHITE = (255, 255 ,255)

pygame.init()

SCREEN = pygame.display.set_mode((600, 600))
CLOCK = pygame.time.Clock()
SCREEN.fill(WHITE)


def transpose(l):
    res = [[0, 0, 0] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            res[i][j] = l[j][i]
    return res


class BaseGame:
    def __init__(self, screen, game_pos=(0, 0), game_size=200) -> None:
        self.SCREEN = screen
        self.grid = np.zeros(shape=(3,3))
        self.game_pos = game_pos
        self.game_size = game_size
        self.grid_image = pygame.image.load("assets/grid.png")
        self.X = pygame.image.load("assets/X.png")
        self.O = pygame.image.load("assets/o.png")
        self.grid_image = pygame.transform.scale(self.grid_image, (self.game_size, self.game_size))
        self.X = pygame.transform.scale(self.X, (self.game_size/5, self.game_size/5))
        self.O = pygame.transform.scale(self.O, (self.game_size/5, self.game_size/5))


    def check_winner(self):
        for n, i in enumerate(self.grid):
            if len(set(i)) == 1 and i[0] != 0:
                self.grid_to_screen((n, 0), (n, 2))
                return i[0]
        for n, i in enumerate(self.grid.T):
            if len(set(i)) == 1 and i[0] != 0:
                self.grid_to_screen((0, n), (2, n))
                return i[0]
        d1 = []
        d2 = []
        for i in range(1, 4):
            d1.append(self.grid[i-1][i-1]) 
            d2.append(self.grid[i-1][-i])
        if len(set(d1)) == 1 and d1[0] != 0:
                self.grid_to_screen((0, 0), (2, 2))
                return d1[0]
        if len(set(d2)) == 1 and d2[0] != 0:
                self.grid_to_screen((0, 2), (2, 0))
                return d2[0]
        return False

    def draw(self):
        self.SCREEN.blit(self.grid_image, (self.game_pos[0]*self.game_size, self.game_pos[1]*self.game_size))
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == 1:
                    self.SCREEN.blit(self.X, ((self.game_size/6) + (self.game_size/3)*(j) - (self.game_size/5)/2 , (self.game_size/6) + (self.game_size/3)*(i) - (self.game_size/5)/2))
                if self.grid[i][j] == 2:
                    self.SCREEN.blit(self.O, ((self.game_size/6) + (self.game_size/3)*(j) - (self.game_size/5)/2 , (self.game_size/6) + (self.game_size/3)*(i) - (self.game_size/5)/2))



    def add(self, symbol, pos):
        x = pos[0] - self.game_pos[1]*self.game_size
        y = pos[1] - self.game_pos[0]*self.game_size

        i, j = x // (self.game_size/3), y // (self.game_size/3)
        i = int(i)
        j = int(j)
        if int(self.grid[i][j]) == 0:
            if symbol == "x":
                self.grid[i][j] = 1
                s = self.X
            else:
                self.grid[i][j] = 2
                s = self.O
            self.SCREEN.blit(
                s, ((self.game_size/6) + (self.game_size/3)*(j) - (self.game_size/5)/2 + self.game_pos[0]*self.game_size, (self.game_size/6) + (self.game_size/3)*(i) - (self.game_size/5)/2 + self.game_pos[1]*self.game_size))
            pygame.display.update()
            return True
        else:
            return False

    def grid_to_screen(self, pos1, pos2):
        i1, j1 = pos1
        i2, j2 = pos2
        spos = ((self.game_size/6) + (self.game_size/3)*(j1) + self.game_pos[0]*self.game_size, (self.game_size/6) + (self.game_size/3)*(i1) + self.game_pos[1]*self.game_size)
        epos = ((self.game_size/6) + (self.game_size/3)*(j2) + self.game_pos[0]*self.game_size, (self.game_size/6) + (self.game_size/3)*(i2) + self.game_pos[1]*self.game_size)
        pygame.draw.line(self.SCREEN, (255, 0, 0), spos, epos, int(self.game_size/30))
        pygame.display.update()


class MainGame:
    def __init__(self) -> None:
        self.SCREEN = SCREEN
        self.grid = [[0, 0, 0] for _ in range(3)]
        self.game_pos = (0, 0)
        self.game_size = 600
        self.grid_image = pygame.image.load("assets/grid.png")
        self.X = pygame.image.load("assets/X.png")
        self.O = pygame.image.load("assets/o.png")
        self.grid_image = pygame.transform.scale(self.grid_image, (self.game_size, self.game_size))
        self.X = pygame.transform.scale(self.X, (self.game_size/5, self.game_size/5))
        self.O = pygame.transform.scale(self.O, (self.game_size/5, self.game_size/5))
        for i in range(3):
            for j in range(3):
                self.grid[i][j] = BaseGame(self.SCREEN, game_pos=(i, j), game_size = int(self.game_size/3))

    def draw(self):
        self.SCREEN.blit(self.grid_image, (self.game_pos[0]*self.game_size, self.game_pos[1]*self.game_size))
        for j in range(3):
            for i in range(3):
                if self.grid[i][j] == 0:
                    continue
                if self.grid[i][j] == 1:
                    self.SCREEN.blit(self.X, ((self.game_size/6) + (self.game_size/3)*(j) - (self.game_size/5)/2 , (self.game_size/6) + (self.game_size/3)*(i) - (self.game_size/5)/2))
                if self.grid[i][j] == 2:
                    self.SCREEN.blit(self.O, ((self.game_size/6) + (self.game_size/3)*(j) - (self.game_size/5)/2 , (self.game_size/6) + (self.game_size/3)*(i) - (self.game_size/5)/2))
                else:
                    self.grid[i][j].draw()
    
    def add(self, symbol, pos):
        x = pos[0] - self.game_pos[1]*self.game_size
        y = pos[1] - self.game_pos[0]*self.game_size

        i, j = x // (self.game_size/3), y // (self.game_size/3)
        i = int(i)
        j = int(j)
        if self.grid[j][i] in [1, 2]:
            return False
        else:
            a = self.grid[j][i].add(symbol, pos)
            if a == True:
                w = self.grid[j][i].check_winner()
                if w != False:
                    self.grid[j][i] = w
                    if symbol == "x":
                        self.grid[j][i] = 1
                        s = self.X
                    else:
                        self.grid[j][i] = 2
                        s = self.O
                    self.SCREEN.blit(
                        s, 
                        (
                            (self.game_size/6) + (self.game_size/3)*(j) - (self.game_size/5)/2 + self.game_pos[0]*self.game_size, 
                            (self.game_size/6) + (self.game_size/3)*(i) - (self.game_size/5)/2 + self.game_pos[1]*self.game_size
                        )
                    )
                pygame.display.update()
                return True
            else:
                return False

    def check_winner(self):
        for n, i in enumerate(self.grid):
            if len(set(i)) == 1 and i[0] != 0:
                self.grid_to_screen((n, 0), (n, 2))
                return i[0]
        for n, i in enumerate(transpose(self.grid)):
            if len(set(i)) == 1 and i[0] != 0:
                self.grid_to_screen((0, n), (2, n))
                return i[0]
        d1 = []
        d2 = []
        for i in range(1, 4):
            d1.append(self.grid[i-1][i-1]) 
            d2.append(self.grid[i-1][-i])
        if len(set(d1)) == 1 and d1[0] != 0:
                self.grid_to_screen((0, 0), (2, 2))
                return d1[0]
        if len(set(d2)) == 1 and d2[0] != 0:
                self.grid_to_screen((0, 2), (2, 0))
                return d2[0]
        return False
    
    def grid_to_screen(self, pos1, pos2):
        j1, i1 = pos1
        j2, i2 = pos2
        spos = ((self.game_size/6) + (self.game_size/3)*(j1) + self.game_pos[0]*self.game_size, (self.game_size/6) + (self.game_size/3)*(i1) + self.game_pos[1]*self.game_size)
        epos = ((self.game_size/6) + (self.game_size/3)*(j2) + self.game_pos[0]*self.game_size, (self.game_size/6) + (self.game_size/3)*(i2) + self.game_pos[1]*self.game_size)
        pygame.draw.line(self.SCREEN, (255, 0, 0), spos, epos, int(self.game_size/30))
        pygame.display.update()
        

def main():
    run = True

    current_x = True
    g = MainGame()
    g.draw()
    pygame.display.update()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if current_x:
                    if g.add("x", (y, x)):
                        current_x = False
                else:
                    if g.add("o", (y, x)):
                        current_x = True

                w = g.check_winner()
                if w != False:
                    run = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

main()

