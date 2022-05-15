import random
import pygame, sys
from pygame.locals import *
import argparse

pygame.init()
frame_rate = pygame.time.Clock()

WIDTH = 600
HEIGHT = 700
WIDTH_TABLE = 400
HEIGHT_TABLE = 400

BLACK = (0,0,0)
GREEN = (0, 255, 0)
GREY = (189, 186, 177)
ANOTHERGREY = (138, 135, 127)
WHITE = (255, 255, 255)

DIMENSIONS = (100, 100)

class Game:

    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        pygame.display.set_caption('2048')
        self.pozitie_initiala=(0,0)
        self.running = True
        self.score = 0
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        self.addTile()
        self.previous = []
        self.prev_points = 0
        for i in range(4):
            self.previous.append(self.grid[i].copy())
        self.highscore = 0
        self.moves = 0

    def run(self):
        running = True
        #self.pozitie_initiala=(random.randint(0,3),random.randint(0,3))
        #x=random.randint(0,10)
        #if x%4==0:
        #    self.grid[self.pozitie_initiala[0]][self.pozitie_initiala[1]]=4
        #else:
        #    self.grid[self.pozitie_initiala[0]][self.pozitie_initiala[1]]=2
        #self.addTile()
        inp = 0
        self.getHighScore()
        while self.running:
            self.draw()
            inp = self.input()
            self.update(inp)
            pygame.display.update()

    def printScore(self):
        background = pygame.Rect(102, 120, 96, 60)
        pygame.draw.rect(self.window, ANOTHERGREY, background, 100)
        font1 = pygame.font.Font('freesansbold.ttf', 12)
        text1 = font1.render("TOTAL POINTS", True, GREY, ANOTHERGREY)
        textRect = text1.get_rect()
        textRect.center = (150, 135)
        font2 = pygame.font.Font('freesansbold.ttf', 20)
        text2 = font2.render(str(self.score), True, WHITE, ANOTHERGREY)
        text2Rect = text2.get_rect()
        text2Rect.center = (150, 160)
        self.window.blit(text1, textRect)
        self.window.blit(text2, text2Rect)

    def printHighScore(self):
        background = pygame.Rect(202, 120, 96, 60)
        pygame.draw.rect(self.window, ANOTHERGREY, background, 100)
        font1 = pygame.font.Font('freesansbold.ttf', 12)
        text1 = font1.render("HIGHSCORE", True, GREY, ANOTHERGREY)
        textRect = text1.get_rect()
        textRect.center = (250, 135)
        font2 = pygame.font.Font('freesansbold.ttf', 20)
        text2 = font2.render(str(self.highscore), True, WHITE, ANOTHERGREY)
        text2Rect = text2.get_rect()
        text2Rect.center = (250, 160)
        self.window.blit(text1, textRect)
        self.window.blit(text2, text2Rect)

    def printMoves(self):
        background = pygame.Rect(302, 120, 96, 60)
        pygame.draw.rect(self.window, ANOTHERGREY, background, 100)
        font1 = pygame.font.Font('freesansbold.ttf', 12)
        text1 = font1.render("MOVES", True, GREY, ANOTHERGREY)
        textRect = text1.get_rect()
        textRect.center = (350, 135)
        font2 = pygame.font.Font('freesansbold.ttf', 20)
        text2 = font2.render(str(self.moves), True, WHITE, ANOTHERGREY)
        text2Rect = text2.get_rect()
        text2Rect.center = (350, 160)
        self.window.blit(text1, textRect)
        self.window.blit(text2, text2Rect)

    def getHighScore(self):
        f = open("highscore.txt", "r")
        self.highscore = int(f.readline())
        f.close()

    def saveHighScore(self):
        f = open("highscore.txt", "w")
        if self.score > self.highscore:
            f.write(str(self.score))
        else:
            f.write(str(self.highscore))
        f.close()

    def draw(self):
        self.window.fill(GREY)
        #self.displayTable()
        for i in range(4):
            for j in range(4):
                tile = pygame.Rect(100 + j * 100, 200 + i * 100, 100, 100)
                pygame.draw.rect(self.window,ANOTHERGREY,tile,100)
                self.printTile((j, i))
        tile = pygame.Rect(96, 196, 408, 408)
        pygame.draw.rect(self.window,ANOTHERGREY,tile,4)
        self.printScore()
        self.printHighScore()
        self.printMoves()
        

    def addTile(self):
        available = []
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    available.append((i, j))
        if random.randint(0, 9) == 0:
            val = 4
        else:
            val = 2

        if len(available) > 0:
            pos = random.choice(available)
            self.grid[pos[0]][pos[1]] = val
            return True
        else:
            return False

    def printTile(self, pos):
        position = (200 + pos[0] * 100 + 1, 100 + pos[1] * 100 + 1)
        image = pygame.image.load(self.getPath(self.grid[pos[0]][pos[1]]))
        image = pygame.transform.scale(image, (94, 94))
        self.window.blit(image, (position[0]-100+2,position[1]+100+2))

    def getPath(self, value):
        return "C:/Users/User/Desktop/2048_Py/Python proiect/images/image_2048_" + str(value) + ".png"

    def rot90(self, grid):
        new_matrix = [[0 for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = grid[3 - j][i]
        return new_matrix

    def rot180(self,grid):
        return self.rot90(self.rot90(grid))

    def rot270(self,grid):
        return self.rot180(self.rot90(grid))

    def fuse(self, positionfrom, positionto, alreadyFused):
        if positionto[1] > 3 or positionto[0] > 3:
            return (False, alreadyFused)
        if positionto[1] < 0 or positionto[0] < 0:
            return (False, alreadyFused)
        if positionfrom[1] > 3 or positionfrom[0] > 3:
            return (False, alreadyFused)
        if positionfrom[1] < 0 or positionfrom[0] < 0:
            return (False, alreadyFused)
        if self.grid[positionfrom[0]][positionfrom[1]] == 0:
            return (False, alreadyFused)
        if self.grid[positionto[0]][positionto[1]] == 0:
            self.grid[positionto[0]][positionto[1]] = self.grid[positionfrom[0]][positionfrom[1]]
            self.grid[positionfrom[0]][positionfrom[1]] = 0
            return (True, alreadyFused)
        if self.grid[positionto[0]][positionto[1]] == self.grid[positionfrom[0]][positionfrom[1]]:
            if not alreadyFused:
                self.grid[positionto[0]][positionto[1]] *= 2
                self.grid[positionfrom[0]][positionfrom[1]] = 0
                self.score += self.grid[positionto[0]][positionto[1]]
                alreadyFused = True
                return (True, alreadyFused)
            else:
                return (False, alreadyFused)
        return (False, alreadyFused)

    def canMove(self, position, alreadyFused):
        if position[1] > 2 or position[0] > 3:
            return 0
        if position[1] < 0 or position[0] < 0:
            return 0
        if self.grid[position[0]][position[1]] == 0:
            return 0
        if self.grid[position[0]][position[1] + 1] == 0:
            return 2
        if self.grid[position[0]][position[1]] == self.grid[position[0]][position[1] + 1]:
            if not alreadyFused:
                return 1
            else:
                return 0

    def movePlace(self, position, direction):
        moved = False
        alreadyFused = False
        ret = (False, False)
        if direction == 'W':
            ret = self.fuse(position, (position[0] - 1, position[1]), alreadyFused)
            while ret[0]:
                alreadyFused = ret[1]
                moved = True
                position = (position[0] - 1, position[1])
                ret = self.fuse(position, (position[0] - 1, position[1]), alreadyFused)
        elif direction == 'S':
            ret = self.fuse(position, (position[0] + 1, position[1]), alreadyFused)
            while ret[0]:
                alreadyFused = ret[1]
                moved = True
                position = (position[0] + 1, position[1])
                ret = self.fuse(position, (position[0] + 1, position[1]), alreadyFused)
        elif direction == 'A':
            ret = self.fuse(position, (position[0], position[1] - 1), alreadyFused)
            while ret[0]:
                alreadyFused = ret[1]
                moved = True
                position = (position[0], position[1] - 1)
                ret = self.fuse(position, (position[0], position[1] - 1), alreadyFused)
        elif direction == 'D':
            ret = self.fuse(position, (position[0], position[1] + 1), alreadyFused)
            while ret[0]:
                alreadyFused = ret[1]
                moved = True
                position = (position[0], position[1] + 1)
                ret = self.fuse(position, (position[0], position[1] + 1), alreadyFused)
        else:
            moved = False
        return moved
        

    def move(self, direction):
        moved = False
        auxiliary = []
        for i in range(4):
            auxiliary.append(self.grid[i].copy())
        aux = self.score
        if direction == 'W':
            for j in range(4):
                for i in range(4):
                    if self.movePlace((i, j), 'W'):
                        moved = True
        elif direction == 'S':
            for j in range(4):
                for i in range(3, -1, -1):
                    if self.movePlace((i, j), 'S'):
                        moved = True
        elif direction == 'A':
            for i in range(4):
                for j in range(4):
                    if self.movePlace((i, j), 'A'):
                        moved = True
        elif direction == 'D':
            for i in range(4):
                for j in range(3, -1, -1):
                    if self.movePlace((i, j), 'D'):
                        moved = True
        else:
            moved = False
        if moved:
            for i in range(4):
                self.previous[i] = auxiliary[i].copy()
            self.prev_points = aux
        return moved

                # if self.grid[i][j] != 0:
                #     if self.grid[i][j] == self.grid[i][j+1]:
                #         self.grid[i][j+1] *= 2
                #     elif self.grid[i][j+1] == 0:
                #         self.grid[i][j+1] = self.grid[i][j]


    # def push(self):
    #     for i in range(4):
    #         for j in range(3):
    #             if self.grid[j][i]!=0:
    #                 if self.grid[j][i] == self.grid[j+1][i]:
    #                     self.grid[j+1][i] = self.grid[j][i] * 2
    #                     self.grid[j][i] = 0
    #                 if(self.grid[j][i] !=0 and self.grid[j+1][i]==0):
    #                     k=j
    #                     while(self.grid[j+1][i]==0 and k<4):
    #                         self.grid[j+1][i]=self.grid[j][i]
    #                         self.grid[j][i]=0
    #                         k=k+1

    # def dreapta(self):
    #     self.move()

    # def sus(self):
    #     self.grid=self.rot270(self.grid)
    #     self.move()
    #     self.grid=self.rot90(self.grid)

    # def stanga(self):
    #     self.grid=self.rot180(self.grid)
    #     self.move()
    #     self.grid=self.rot180(self.grid)

    # def jos(self):
    #     self.grid=self.rot90(self.grid)
    #     self.move()
    #     self.grid=self.rot270(self.grid)

    def undo(self):
        if self.grid != self.previous:
            self.moves = self.moves - 1
            self.score = self.prev_points
        for i in range(4):
            self.grid[i] = self.previous[i].copy()
    
    def update(self, input):
        if input == 'U':
            self.undo()
        else:
            moved = self.move(input)
            if moved:
                self.addTile()
                self.moves = self.moves + 1

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.saveHighScore()
                sys.exit()
            if event.type==KEYDOWN:
                if event.key == K_UP:
                    return 'A'
                elif event.key == K_DOWN:
                    return 'D'
                elif event.key == K_LEFT:
                    return 'W'
                elif event.key == K_RIGHT:
                    return 'S'
                elif event.key == K_u:
                    return 'U'

def main():
    game = Game()
    game.run()
    pass

main()
