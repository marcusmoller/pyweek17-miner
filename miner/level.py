import pygame
import time
import random

from player import player
from block import BlockSprite
from resource import ResourceSprite
from constants import BLOCK_W, BLOCK_H, RESOURCE_MAX_W, DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT

class LevelEngine():
    def __init__(self):
        self.blocks = pygame.sprite.Group()

        self.levelStructure = [[None for i in range(50)] for i in range(50)]
        self.resources = []

        # player
        self.blocksAroundPlayer = []

        # level time
        self.levelTime = 0
        self.levelTimeStart = time.time()
        self.levelTimeLeft = 0

        # level score
        self.requiredResources = 0

    def generateLevel(self, levelTime):
        self.levelTime = levelTime
        self.levelTimeStart = time.time()
        self.levelTimeLeft = levelTime

        self.requiredResources = int(levelTime / 10 * 1.5)

        maxHeight = 4

        # fill everything
        for x in range(34):
            for y in range(30):
                if y < 15:
                    # make space for player
                    continue

                # make some blocks resource rich
                altitude = y - 15

                rnd = random.randint(0, 400/y)
                if rnd == 0:
                    tempBlock = BlockSprite(x*BLOCK_W, y*BLOCK_H, isResourceRich=True)
                else:
                    tempBlock = BlockSprite(x*BLOCK_W, y*BLOCK_H)

                self.blocks.add(tempBlock)
                self.levelStructure[x][y] = tempBlock

        # generate terrain
        for x in range(30):
            i = random.randint(0, 4)

            for y in range(i):
                y += 15
                tempBlock = BlockSprite(x*BLOCK_W, (y-i)*BLOCK_H)
                self.blocks.add(tempBlock)
                self.levelStructure[x][y-i] = tempBlock

        self.calculateOuterBlocks()

    def calculateOuterBlocks(self):
        for x in range(len(self.levelStructure)):
            for y in range(30):
                block = self.levelStructure[x][y]
                if block != None:
                    block.isBorder = False
                    if self.levelStructure[x][y-1] is None:
                        # top
                        #block.borderTop()
                        block.borders[DIR_UP] = True
                        block.isBorder = True
                    if self.levelStructure[x][y+1] is None:
                        # bottom
                        #block.borderBottom()
                        block.borders[DIR_DOWN] = True
                        block.isBorder = True
                    if self.levelStructure[x-1][y] is None:
                        # left
                        #block.borderLeft()
                        block.borders[DIR_LEFT] = True
                        block.isBorder = True
                    if self.levelStructure[x+1][y] is None:
                        # right
                        #block.borderRight()
                        block.isBorder = True
                        block.borders[DIR_RIGHT] = True

    def calculateBlocksAroundPlayer(self):
        blocks = []
        plrX = player.rect.x // player.rect.w
        plrY = player.rect.y // player.rect.h

        blocks.append(self.levelStructure[plrX][plrY])

        blocks.append(self.levelStructure[plrX][plrY-1]) # above
        blocks.append(self.levelStructure[plrX+1][plrY-1]) # above right
        blocks.append(self.levelStructure[plrX+1][plrY]) # right
        blocks.append(self.levelStructure[plrX+1][plrY+1]) # below right
        blocks.append(self.levelStructure[plrX][plrY+1]) # below
        blocks.append(self.levelStructure[plrX-1][plrY+1]) # below left
        blocks.append(self.levelStructure[plrX-1][plrY]) # left
        blocks.append(self.levelStructure[plrX-1][plrY-1]) # above left

        self.blocksAroundPlayer = blocks

    def destroyBlock(self, (x, y)):
        if self.levelStructure[x][y] is not None:
            # check if the block is resource rich
            if self.levelStructure[x][y].isResourceRich:
                chance = 1
            else:
                chance = random.randint(0, 20)

            # spawn resources
            xPos = random.randint(x*BLOCK_W, (x*BLOCK_W+BLOCK_W)-RESOURCE_MAX_W)
            self.spawnResources(xPos, y*BLOCK_H+2, chance)

            # remove block
            self.levelStructure[x][y] = None
            self.calculateOuterBlocks()


    def spawnBlock(self, (x, y)):
        if self.levelStructure[x][y] is None:
            self.levelStructure[x][y] = BlockSprite(x*BLOCK_W, (y)*BLOCK_H)
            self.calculateOuterBlocks()

    def spawnResources(self, x, y, chance):
        if chance == 1:
            self.resources.append(ResourceSprite(x, y))

    def resetTimer(self):
        self.levelTimeStart = time.time()

level = LevelEngine()