import pygame

from miner.constants import *

class BlockSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, isResourceRich=False):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([BLOCK_W, BLOCK_H])
        self.image.fill(BLOCK_COLOR)

        self.isBorder = False
        self.borderImage = pygame.Surface([BLOCK_W, BLOCK_H])
        self.borderImage.fill(BLOCK_COLOR_BORDER)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.isResourceRich = isResourceRich
        if isResourceRich:
            self.image.fill(BLOCK_COLOR_RICH)

        self.borders = [False, False, False, False]

    def draw(self, surface):
        if not self.isBorder:
            surface.blit(self.image, self.rect)

        elif self.isBorder and self.isResourceRich:
            surface.blit(self.image, self.rect)

        elif self.isBorder:
            surface.blit(self.borderImage, self.rect)
