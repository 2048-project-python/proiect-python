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
DIMENSIONS = (100, 100)

class Place:
    def __init__(self,  position):
        self.dimensions = DIMENSIONS
        self.position = position
        self.value = 0

    def getValue(self):
        return self.value

    def getLine(self):
        return self.position[0]

    def getColumn(self):
        return self.position[1]

    def hasValue(self):
        return (self.value != 0)

    def setValue(self, value):
        self.value = value

    def setPosition(self, position):
        self.position = position

    def print(self):
        s = "(" + str(self.position[0]) + ", " + str(self.position[1]) + ") - " + str(self.value)
        print(s)

    def draw(self):
        tile = pygame.Rect(100 + self.position[1] * 100, 200 + self.position[0] * 100, 100, 100)
        surf = pygame.Surface((100, 100))
        pygame.draw.rect(surf, GREEN, tile,2)

class Game:

    
    def run(self):
        running = True
        while running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        pygame.display.set_caption('2048')
        self.Place=[]
        self.running = True
        self.score = 0
        self.grid = [[Place((i, j)) for i in range(4)] for j in range(4)]
        self.addTile()

    def draw(self):
        self.window.fill(GREEN)
        #self.displayTable()
        for i in self.Place:
            self.draw()

    def displayTable(self):
        for i in range(4):
            for j in range(4):
                self.grid[i][j].draw()

    def addTile(self, position = (-1, -1), value = -1):
        pass

def main():
    game = Game()
    game.run()

    pass


main()