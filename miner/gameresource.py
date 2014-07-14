import pygame
import random

from miner.constants import RESOURCE_MAX_W, RESOURCE_MAX_H, \
    RESOURCE_COLORS, MOVEMENT_SPEED


class ResourceSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        w = random.randint(5, RESOURCE_MAX_W)
        h = random.randint(4, RESOURCE_MAX_H)
        self.image = pygame.Surface([w, h])

        # random color
        color = random.randint(0, len(RESOURCE_COLORS) - 1)
        self.image.fill(RESOURCE_COLORS[color])

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.xVel = 0
        self.yVel = 0

        self.onGround = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        ''' THIS IS UNUSED - SEE engine.py'''

        # handle gravity (assume it's not on ground)
        self.onGround = False
        if not self.onGround:
            self.yVel = 1

        self.rect.y += self.yVel
