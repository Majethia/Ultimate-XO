import sys
import numpy as np
import pygame

WHITE = (255, 255 ,255)
SCREEN = pygame.display.set_mode((600, 600))
CLOCK = pygame.time.Clock()
SCREEN.fill(WHITE)

class BaseGame:
    def __init__(self, screen, game_pos=(0, 0), game_size=800) -> None:
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
                s, 
                (
                    (self.game_size/6) + (self.game_size/3)*(j) - (self.game_size/5)/2 + self.game_pos[0]*self.game_size, 
                    (self.game_size/6) + (self.game_size/3)*(i) - (self.game_size/5)/2 + self.game_pos[1]*self.game_size
            )
        )

    def grid_to_screen(self, pos1, pos2):
        i1, j1 = pos1
        i2, j2 = pos2
        spos = ((self.game_size/6) + (self.game_size/3)*(j1) + self.game_pos[0]*self.game_size, (self.game_size/6) + (self.game_size/3)*(i1) + self.game_pos[1]*self.game_size)
        epos = ((self.game_size/6) + (self.game_size/3)*(j2) + self.game_pos[0]*self.game_size, (self.game_size/6) + (self.game_size/3)*(i2) + self.game_pos[1]*self.game_size)
        pygame.draw.line(self.SCREEN, (255, 0, 0), spos, epos, int(self.game_size/30))


def main():
    run = True
    g = BaseGame(SCREEN, game_size=600, game_pos=(0, 0))
    current_x = True
    g.draw()
    while run:
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

        pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()
