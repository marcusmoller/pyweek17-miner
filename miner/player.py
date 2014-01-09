import pygame

from miner.constants import *

class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([BLOCK_W, BLOCK_H+4]) # make the player sprite a little taller than the blocks, but NOT the rect
        self.image.fill(PLAYER_COLOR)

        #self.rect = self.image.get_rect()
        self.rect = pygame.Rect((0, 0, BLOCK_W, BLOCK_H))
        self.rect.x = 10
        self.rect.y = 250

        self.xVel = 0
        self.yVel = 0

        # jumping
        self.jumping = False
        self.onGround = False
        self.origJumpVel = 3.5
        self.jumpVel = self.origJumpVel
        self.gravity = 0.1

        # targetting
        self.direction = DIR_RIGHT
        self.directionOld = DIR_RIGHT
        self.targetBlock = (None, None)

        # score
        self.altitude = 0
        self.collectedResources = 0

    def draw(self, surface):
        y = self.rect.y + (self.rect.h - self.image.get_rect().h)
        surface.blit(self.image, (self.rect.x, y))

    def update(self):
        ''' THIS IS UNUSED - SEE engine.py'''
        # handle jump 
        self.doJump()

        # handle gravity (assume we're not on ground)
        self.onGround = False
        if not self.onGround and not self.jumping:
            self.yVel = 2


        # move player
        if self.xVel < -MOVEMENT_SPEED:
            self.xVel = -MOVEMENT_SPEED
        elif self.xVel > MOVEMENT_SPEED:
            self.xVel = MOVEMENT_SPEED

        self.rect.x += self.xVel
        self.rect.y += self.yVel

    def reset(self):
        self.rect.x = PLAYER_START_X
        self.rect.y = PLAYER_START_Y

        self.xVel = 0
        self.yVel = 0
        self.direction = DIR_RIGHT

        self.collectedResources = 0


    def doJump(self):
        if self.jumping and not self.onGround:
            self.yVel = -self.jumpVel
            self.jumpVel -= self.gravity

        #if not self.onGround:
        #   self.yVel -= 4

        if self.onGround:
            self.jumping = False
            self.jumpVel = self.origJumpVel
            self.yVel = 0
            self.onGround = True


# define player
player = PlayerSprite()
