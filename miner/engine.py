import pygame
import time

from miner.menus import *
from miner.player import player
from miner.level import level
from miner.graphics import GraphicsEngine
from miner.constants import *


class GameEngine():
    def __init__(self, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        # screen
        self.screen = None

        # menu state
        self.GAME_STATE = MENU_STARTGAME

        # game
        self.clock = pygame.time.Clock()
        self.gameTime = time.time()
        self.gameRunning = True
        self.currentLevel = 1

    def initializeGame(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            [self.screenWidth, self.screenHeight])
        pygame.display.set_caption('MINER')

        # engines
        self.graphicsEngine = GraphicsEngine(self.screen)

        # menus
        self.menuStartGame = MenuStartGame(self.screen, self)
        self.menuAbout = MenuAbout(self.screen, self)
        self.menuScene = MenuScene(self.screen, self)
        self.menuGameOver = MenuGameOver(self.screen, self)
        self.menuGameFinish = MenuGameFinish(self.screen, self)

        # start the loop
        self.gameLoop()

    def gameLoop(self):
        while self.gameRunning:
            if self.GAME_STATE == MENU_STARTGAME:
                self.menuStartGame.draw()
                self.menuStartGame.update()

            elif self.GAME_STATE == MENU_ABOUT:
                self.menuAbout.draw()
                self.menuAbout.update()

            elif self.GAME_STATE == MENU_SCENE:
                self.menuScene.draw()
                self.menuScene.update()

            elif self.GAME_STATE == MENU_GAMEOVER:
                self.menuGameOver.draw()
                self.menuGameOver.update()

            elif self.GAME_STATE == MENU_GAMEFINISH:
                self.menuGameFinish.draw()
                self.menuGameFinish.update()

            elif self.GAME_STATE == MENU_INGAME:
                # handle input
                pygame.event.pump()
                for event in pygame.event.get():
                    self.handleInput(event)

                    if event.type == pygame.QUIT:
                        self.gameRunning = False
                        break

                # update everything
                self.playerMove()

                for resource in level.resources:
                    resource.update()
                    self.checkCollision(resource, 0, resource.yVel)

                self.checkResourceCollision()

                level.levelTimeLeft = level.levelTime - (time.time() -
                                                         level.levelTimeStart)
                self.checkGameState()

                # draw everything
                self.graphicsEngine.renderGame()
                pygame.display.update()

                # limit fps
                self.clock.tick(60)

        # game not running any longer, so lets quit
        pygame.quit()

    def handleInput(self, event):
        global player

        def pressed(key):
            keys = pygame.key.get_pressed()

            if keys[key]:
                return True
            else:
                return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.direction = DIR_UP

            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.xVel = -MOVEMENT_SPEED
                player.direction = DIR_LEFT

            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.xVel = +MOVEMENT_SPEED
                player.direction = DIR_RIGHT

            # jump
            elif event.key == pygame.K_x:
                player.jumping = True
                player.onGround = False

            # mine
            elif event.key == pygame.K_c:
                level.destroyBlock(
                    player.targetBlock[0], player.targetBlock[1])

            # spawn block
            elif event.key == pygame.K_v:
                if player.collectedResources >= 4:
                    level.spawnBlock(
                        player.targetBlock[0], player.targetBlock[1])
                    player.collectedResources -= 4

            # exit
            elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                self.gameRunning = False

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.direction = player.directionOld

            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.direction = player.directionOld

            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.xVel += MOVEMENT_SPEED
                player.direction = DIR_LEFT

            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.xVel -= MOVEMENT_SPEED
                player.direction = DIR_RIGHT

        if pressed(pygame.K_DOWN) or pressed(pygame.K_s):
            if player.direction != DIR_DOWN and player.direction != DIR_UP:
                player.directionOld = player.direction
            player.direction = DIR_DOWN

        if pressed(pygame.K_UP) or pressed(pygame.K_w):
            if player.direction != DIR_DOWN and player.direction != DIR_UP:
                player.directionOld = player.direction
            player.direction = DIR_UP

        if pressed(pygame.K_l):
            player.collectedResources += 1

    def setState(self, state):
        if state == MENU_INGAME:
            # reset game information
            level.generateLevel(90 - (self.currentLevel * 10))

            player.reset()

        self.GAME_STATE = state

    def resetGame(self):
        self.currentLevel = 1
        self.menuScene.currentScene = 0

        level.generateLevel(90 - (self.currentLevel * 10))
        player.reset()

    def checkGameState(self):
        # check game over
        if level.levelTimeLeft <= 0:
            self.setState(MENU_GAMEOVER)
        else:
            # check game score
            if (player.collectedResources >= level.requiredResources and
                    player.altitude >= 0 and not player.jumping):
                # player has completed the level
                self.currentLevel += 1

                if (len(self.menuScene.scenes) >
                        self.menuScene.currentScene + 1):
                    self.menuScene.currentScene += 1
                    self.setState(MENU_SCENE)

    def checkCollision(self, sprite, xVel, yVel):
        for x in range(len(level.levelStructure)):
            for y in range(len(level.levelStructure[x])):
                block = level.levelStructure[x][y]

                if block is not None:
                    if pygame.sprite.collide_rect(sprite, block):
                        if xVel < 0:
                            sprite.rect.x = block.rect.x + block.rect.w

                        if xVel > 0:
                            sprite.rect.x = block.rect.x - sprite.rect.w

                        if yVel < 0:
                            sprite.rect.y = block.rect.y + block.rect.h

                        if yVel > 0 and not sprite.onGround:
                            sprite.onGround = True
                            sprite.rect.y = block.rect.y - sprite.rect.h

        '''for block in level.blocksAroundPlayer:
            if block is not None:
                if pygame.sprite.collide_rect(player, block):
                    if xVel < 0:
                        player.rect.x = block.rect.x + block.rect.w

                    if xVel > 0:
                        player.rect.x = block.rect.x - player.rect.w

                    if yVel < 0:
                        player.rect.y = block.rect.y + block.rect.h

                    if yVel > 0 and not player.onGround:
                        player.onGround = True
                        player.rect.y = block.rect.y - player.rect.h'''

    def checkResourceCollision(self):
        for resource in level.resources:
            if pygame.sprite.collide_rect(player, resource):
                level.resources.remove(resource)
                player.collectedResources += 1

    def playerMove(self):
        ''' this is done in GameEngine due to collision problems '''
        #level.calculateBlocksAroundPlayer()

        # set altitude
        player.altitude = 15 - (player.rect.y + player.rect.h) // BLOCK_H

        player.doJump()

        player.onGround = False
        if not player.onGround and not player.jumping:
            player.yVel = 4

        if player.xVel > MOVEMENT_SPEED:
            player.xVel = MOVEMENT_SPEED
        elif player.xVel < -MOVEMENT_SPEED:
            player.xVel = -MOVEMENT_SPEED

        if player.rect.x <= 0:
            player.rect.x = 0
        elif player.rect.x >= SCREEN_WIDTH - player.rect.w:
            player.rect.x = SCREEN_WIDTH - player.rect.w

        # move player and check collision
        player.rect.x += player.xVel
        self.checkCollision(player, player.xVel, 0)
        player.rect.y += player.yVel
        self.checkCollision(player, 0, player.yVel)
