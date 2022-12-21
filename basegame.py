import sys
import numpy as np
import pygame

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
        self.winpos = None

    def check_winner(self):
        has_empty = False
        for i in self.grid:
            for j in i:
                if j == 0:
                    has_empty = True

        for n, i in enumerate(self.grid):
            if len(set(i)) == 1 and i[0] != 0:
                self.winpos = ((n, 0), (n, 2))
                return i[0]
        for n, i in enumerate(self.grid.T):
            if len(set(i)) == 1 and i[0] != 0:
                self.winpos = ((0, n), (2, n))
                return i[0]
        d1 = []
        d2 = []
        for i in range(1, 4):
            d1.append(self.grid[i-1][i-1]) 
            d2.append(self.grid[i-1][-i])
        if len(set(d1)) == 1 and d1[0] != 0:
                self.winpos = ((0, 0), (2, 2))
                return d1[0]
        if len(set(d2)) == 1 and d2[0] != 0:
                self.winpos = ((0, 2), (2, 0))
                return d2[0]
        self.winpos = None
        if not has_empty:
            return 'tie' 
        return False

    def draw(self):
        self.SCREEN.blit(self.grid_image, (self.game_pos[0]*self.game_size, self.game_pos[1]*self.game_size))
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == 1:
                    self.SCREEN.blit(self.X, ((self.game_size/6) + (self.game_size/3)*(j) - (self.game_size/5)/2 , (self.game_size/6) + (self.game_size/3)*(i) - (self.game_size/5)/2))
                if self.grid[i][j] == 2:
                    self.SCREEN.blit(self.O, ((self.game_size/6) + (self.game_size/3)*(j) - (self.game_size/5)/2 , (self.game_size/6) + (self.game_size/3)*(i) - (self.game_size/5)/2))
        if self.winpos != None:
            self.grid_to_screen(self.winpos)

    def add(self, symbol, pos):
        x = pos[0] - self.game_pos[1]*self.game_size
        y = pos[1] - self.game_pos[0]*self.game_size

        i, j = x // (self.game_size/3), y // (self.game_size/3)
        i = int(i)
        j = int(j)
        if int(self.grid[i][j]) == 0:
            if symbol == "x":
                self.grid[i][j] = 1
            else:
                self.grid[i][j] = 2

    def grid_to_screen(self, pos):
        i1, j1 = pos[0]
        i2, j2 = pos[1]
        spos = ((self.game_size/6) + (self.game_size/3)*(j1) + self.game_pos[0]*self.game_size, (self.game_size/6) + (self.game_size/3)*(i1) + self.game_pos[1]*self.game_size)
        epos = ((self.game_size/6) + (self.game_size/3)*(j2) + self.game_pos[0]*self.game_size, (self.game_size/6) + (self.game_size/3)*(i2) + self.game_pos[1]*self.game_size)
        pygame.draw.line(self.SCREEN, (255, 0, 0), spos, epos, int(self.game_size/30))

    def best_move(self):
        max_score = float('-inf')
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == 0:
                    self.grid[i][j] = 2
                    score = self.minimax(False)
                    self.grid[i][j] = 0
                    if max_score < score:
                        max_score = score
                        best_move = (i, j)
        return best_move

    def minimax(self, is_max):
        w = self.check_winner()
        if w != False:
            return {1: -1, 2: 1, 'tie': 0}[w] # 1 == x and 2 == o

        if is_max:
            max_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if self.grid[i][j] == 0:
                        self.grid[i][j] = 2
                        score = self.minimax(False)
                        self.grid[i][j] = 0
                        max_score = max(score, max_score)
            return max_score

        else:
            min_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.grid[i][j] == 0:
                        self.grid[i][j] = 1
                        score = self.minimax(True)
                        self.grid[i][j] = 0
                        min_score = min(score, min_score)
            return min_score

