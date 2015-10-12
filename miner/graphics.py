import pygame
import random

from miner.player import player
from miner.level import level
from miner.data import filepath
from miner.constants import *


class GraphicsEngine():
    def __init__(self, surface):
        self.screenSurface = surface

        # sprite groups
        self.allSprites = pygame.sprite.Group()
        #self.allSprites.add(level.blocks)
        self.allSprites.add(player)

        # star field
        self.stars = []
        self.initializeStarfield()

        # load everything
        self.loadResources()

    def loadResources(self):
        # sprites
        self.spriteAim = pygame.image.load(filepath(
            'aim.png')).convert_alpha()
        self.spriteEarth = pygame.image.load(filepath(
            'earth.png')).convert_alpha()

        # fonts
        self.scoreFont = pygame.font.Font(filepath('Minecraftia.ttf'), 16)

    def initializeStarfield(self):
        for i in range(MAX_STARS):
            star = [random.randint(0, SCREEN_WIDTH), random.randint(
                0, SCREEN_HEIGHT), 1]
            self.stars.append(star)

    def renderGame(self):
        self.screenSurface.fill((0, 0, 0))
        self.drawStarfield()
        self.drawEarth()

        # draw blocks
        for x in range(50):
            for y in range(50):
                block = level.levelStructure[x][y]
                if block is not None:
                    block.draw(self.screenSurface)

        # draw resources
        for resource in level.resources:
            resource.draw(self.screenSurface)

        # draw player aim
        self.drawPlayerAim()

        # draw player
        #self.allSprites.draw(self.screenSurface)
        player.draw(self.screenSurface)

        # draw score
        self.drawScore()
        self.drawTime()
        self.drawAltitude()

    def drawStarfield(self):
        for star in self.stars:
            self.screenSurface.fill((255, 255, 255), (star[0], star[1],
                                    star[2], star[2]))

    def drawEarth(self):
        if level.levelTime == level.levelTimeLeft:
            self.screenSurface.blit(self.spriteEarth, (400, 300))
        else:
            self.screenSurface.blit(self.spriteEarth, (400, 300 /
                                    level.levelTime * (level.levelTime -
                                                       level.levelTimeLeft)))

    def drawScore(self):
        textSurface = self.scoreFont.render('RESOURCES: ' +
            str(player.collectedResources) + '/' +
            str(level.requiredResources), 0, (255, 255, 255))
        self.screenSurface.blit(textSurface, (20, 20))

    def drawTime(self):
        textSurface = self.scoreFont.render('TIME LEFT: ' + str(round(
            level.levelTimeLeft, 1)) + ' SECS', 0, (255, 255, 255))
        self.screenSurface.blit(textSurface, (20, 44))

    def drawAltitude(self):
        textSurface = self.scoreFont.render('ALTITUDE: ' + str(
            player.altitude) + ' m', 0, (255, 255, 255))
        self.screenSurface.blit(textSurface, (20, 68))

    def drawPlayerAim(self):
        # calculate rect based on player direction
        imageRect = self.spriteAim.get_rect()
        if player.direction == DIR_UP:
            imageRect.x = ((player.rect.centerx) // BLOCK_W) * BLOCK_W
            imageRect.y = (player.rect.centery -
                           BLOCK_H) // BLOCK_H * BLOCK_H

        elif player.direction == DIR_DOWN:
            imageRect.x = ((player.rect.centerx) // BLOCK_W
                           ) * BLOCK_W
            imageRect.y = (player.rect.centery +
                           player.rect.h) // BLOCK_H * BLOCK_H

        elif player.direction == DIR_LEFT:
            imageRect.x = ((player.rect.centerx -
                           player.rect.w) // BLOCK_W) * BLOCK_W
            imageRect.y = (player.rect.centery +
                           (player.rect.h - BLOCK_H)) // BLOCK_H * BLOCK_H

        elif player.direction == DIR_RIGHT:
            imageRect.x = ((player.rect.centerx + player.rect.w) //
                           BLOCK_W * BLOCK_W)
            imageRect.y = (player.rect.centery + (player.rect.h - BLOCK_H)
                           ) // BLOCK_H * BLOCK_H

        # set player target block
        player.targetBlock = (imageRect.x // BLOCK_W, imageRect.y // BLOCK_H)

        # draw crosshair
        self.screenSurface.blit(self.spriteAim, imageRect)
