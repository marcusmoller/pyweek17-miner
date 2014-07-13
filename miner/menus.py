import pygame
import sys

from miner.data import filepath
from miner.constants import *


class MenuClass():
    def __init__(self, surface):
        '''menu object
        '''
        self.surface = surface

        self.backgroundColor = (0, 0, 0)

        # font
        self.textFont = pygame.font.Font(filepath('Minecraftia.ttf'), 16)

        # menus
        self.selectedMenu = 0
        self.menus = []

        # texts
        self.texts = []

        # keyboard events
        self.keyboardEvents = []

    def draw(self):
        self.surface.fill(self.backgroundColor)

        if len(self.menus) != 0:
            self.drawMenus()

        # update surface
        pygame.display.update()

    def drawMenus(self):
        for menu in self.menus:
            menu.draw(self.surface)

    def update(self):
        for event in pygame.event.get():
            self._handleEvents(event)

    def _handleEvents(self, event):
        def pressed(key):
            keys = pygame.key.get_pressed()

            if keys[key]:
                return True
            else:
                return False

        if pressed(pygame.K_UP):
            if self.selectedMenu <= 0:
                self.selectedMenu = len(self.menus) - 1
            else:
                self.selectedMenu -= 1

            self._updateSelectedMenu()

        if pressed(pygame.K_DOWN):
            if self.selectedMenu >= (len(self.menus) - 1):
                self.selectedMenu = 0
            else:
                self.selectedMenu += 1

            self._updateSelectedMenu()

        if pressed(pygame.K_SPACE) or pressed(pygame.K_RETURN) or pressed(
                pygame.K_x):
            if len(self.menus) != 0:
                self.menus[self.selectedMenu].click()

        if pressed(pygame.K_q) or pressed(pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

    def addMenu(self, caption, fgColor=(255, 255, 255)):
        self.menus.append(MenuItemClass(caption, fgColor=fgColor))

        # update placement (center)
        menuAmount = len(self.menus)
        for i in range(len(self.menus)):
            self.menus[i].rect.centerx = SCREEN_WIDTH / 2
            self.menus[i].rect.centery = SCREEN_HEIGHT / (
                menuAmount + 1) * (i + 1)

        self._updateSelectedMenu()

    def _updateSelectedMenu(self):
        for menu in self.menus:
            if self.menus.index(menu) == self.selectedMenu:
                menu.select()
            else:
                menu.deselect()


class MenuItemClass(pygame.sprite.Sprite):
    def __init__(self, caption='', antialias=0, fgColor=(255, 255, 255)):
        pygame.sprite.Sprite.__init__(self)

        self.caption = caption
        self.antialias = antialias
        self.fgColor = fgColor

        self.font = pygame.font.Font(filepath('Minecraftia.ttf'), 32)

        self.image = self.font.render(self.caption, antialias, fgColor)
        self.rect = self.image.get_rect()

        self.event = None

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def select(self):
        self.image = self.font.render(
            self.caption, self.antialias, (100, 100, 100))

    def deselect(self):
        self.image = self.font.render(
            self.caption, self.antialias, self.fgColor)

    def click(self):
        if self.event is not None:
            self.event()

    def connect(self, action):
        self.event = action


class MenuStartGame(MenuClass):
    def __init__(self, surface, engine):
        '''menus
        '''
        MenuClass.__init__(self, surface)

        self.engine = engine

        self.addMenu('Start')
        self.menus[0].connect(self.clickStart)

        self.addMenu('About')
        self.menus[1].connect(self.clickAbout)

        self.addMenu('Quit')
        self.menus[2].connect(self.clickQuit)

    def clickStart(self):
        self.engine.GAME_STATE = MENU_SCENE

    def clickAbout(self):
        self.engine.setState(MENU_ABOUT)

    def clickQuit(self):
        pygame.quit()
        sys.exit()


class MenuScene(MenuClass):
    def __init__(self, surface, engine):
        MenuClass.__init__(self, surface)

        self.engine = engine

        self.currentScene = 0

        self.scenes = ['Good morning Sam.\nHow are you feeling today?',

        'Your final mission before going home to Earth,\n'
        'is to gather the requested RESOURCES.\n\nI sincerely hope your'
        ' enjoy your last week and\nI hope life on Earth is exactly'
        ' how you remember it to be.',

        'You will have a 5% chance of finding RESOURCES in a '
        'regular moon rock,\nand a 100% chance in rich moon rocks.\n\n'
        'Our scans tell us that the deeper you dig,\n'
        'the more resource rich rocks you will locate.\n\n'
        'You should spend your time wisely.',

        '... and remember Sam.\n'
        'You must reach an ALTITUDE of above 0 afterwards\n'
        'or we will not be able to pick you up.',

        'CONTROLS:\nArrow keys for movement and aiming\n'
        'X for jumping\n'
        'C for destroying blocks\n'
        'V for creating blocks (requires 4 RESOURCES)',

        'Well done. I am sure your family back home on '
        'Earth is proud of you.\n'
        'Are you excited to go back to them?'
        '\nSam, get some sleep. You are very tired.',

        'You are really close to going back now.\n'
        'Are you not happy to hear that?',

        'I am going to miss you Sam. I want you to know that.\n'
        'Maybe the next one will be like you.\n\nWe will see...',

        'Sam.... you do not look too well. How are you feeling?\n'
        '\nAre you feeling okay?',

        'Sam... Sam...\nCan you hear me? Sam?\n\n*Contacting the company*\n'
        'Sam #073 is dead.\nRequesting the assistance of Sam #074 ASAP.']

    def draw(self):
        self.surface.fill(self.backgroundColor)

        self.renderText()
        self.drawHint()

        # update surface
        pygame.display.update()

    def _handleEvents(self, event):
        def pressed(key):
            keys = pygame.key.get_pressed()

            if keys[key]:
                return True
            else:
                return False

        if pressed(pygame.K_x):
            self.nextScene()

    def nextScene(self):
        if self.currentScene < 4:
            # li
            self.currentScene += 1
        elif self.currentScene == 9:
            self.engine.resetGame()
            self.engine.setState(MENU_GAMEFINISH)
        else:
            self.engine.setState(MENU_INGAME)

    def renderText(self):
        # split texts at \n (newline)

        texts = self.scenes[self.currentScene].split('\n')

        for i in range(len(texts)):
            textSurface = self.textFont.render(texts[i], 0, (255, 255, 255))

            textRect = textSurface.get_rect()
            textRect.centerx = SCREEN_WIDTH / 2
            textRect.centery = SCREEN_HEIGHT / 2 + i * self.textFont.size(
                texts[i])[1]

            self.surface.blit(textSurface, textRect)

    def drawHint(self):
        textSurface = self.textFont.render(
            '(Click X to continue)', 0, (255, 255, 255))
        textRect = textSurface.get_rect()
        textRect.centerx = SCREEN_WIDTH / 2
        textRect.centery = SCREEN_HEIGHT - 50
        self.surface.blit(textSurface, textRect)


class MenuAbout(MenuClass):
    def __init__(self, surface, engine):
        MenuClass.__init__(self, surface)

        self.engine = engine

        self.currentScene = 0

        self.text = ('ABOUT\nMINER is a PyWeek entry by Marcus Moller.\n'
            'Written in Python (2.7) and PyGame.\n\nmarcusmoller @ GitHub')

    def draw(self):
        self.surface.fill(self.backgroundColor)

        self.renderText()
        self.drawHint()

        # update surface
        pygame.display.update()

    def _handleEvents(self, event):
        def pressed(key):
            keys = pygame.key.get_pressed()

            if keys[key]:
                return True
            else:
                return False

        if pressed(pygame.K_ESCAPE):
            self.engine.setState(MENU_STARTGAME)

    def renderText(self):
        # split texts at \n (newline)

        texts = self.text.split('\n')

        for i in range(len(texts)):
            textSurface = self.textFont.render(texts[i], 0, (255, 255, 255))

            textRect = textSurface.get_rect()
            textRect.centerx = SCREEN_WIDTH / 2
            textRect.centery = SCREEN_HEIGHT / 2 + i * self.textFont.size(
                texts[i])[1]

            self.surface.blit(textSurface, textRect)

    def drawHint(self):
        textSurface = self.textFont.render(
            '(Click ESC to return)', 0, (255, 255, 255))
        textRect = textSurface.get_rect()
        textRect.centerx = SCREEN_WIDTH / 2
        textRect.centery = SCREEN_HEIGHT - 50
        self.surface.blit(textSurface, textRect)


class MenuGameOver(MenuClass):
    def __init__(self, surface, engine):
        MenuClass.__init__(self, surface)

        self.engine = engine

        self.text = ('... Sam.\n'
        'You failed.\n\nYou will never make it back to Earth now.')

    def draw(self):
        self.surface.fill(self.backgroundColor)

        self.renderText()
        self.drawHint()

        # update surface
        pygame.display.update()

    def _handleEvents(self, event):
        def pressed(key):
            keys = pygame.key.get_pressed()

            if keys[key]:
                return True
            else:
                return False

        if pressed(pygame.K_x):
            self.engine.setState(MENU_STARTGAME)

    def renderText(self):
        # split texts at \n (newline)

        texts = self.text.split('\n')

        for i in range(len(texts)):
            textSurface = self.textFont.render(texts[i], 0, (255, 255, 255))

            textRect = textSurface.get_rect()
            textRect.centerx = SCREEN_WIDTH / 2
            textRect.centery = SCREEN_HEIGHT / 2 + i * self.textFont.size(
                texts[i])[1]

            self.surface.blit(textSurface, textRect)

    def drawHint(self):
        textSurface = self.textFont.render(
            '(Click X to return to main screen)', 0, (255, 255, 255))
        textRect = textSurface.get_rect()
        textRect.centerx = SCREEN_WIDTH / 2
        textRect.centery = SCREEN_HEIGHT - 50
        self.surface.blit(textSurface, textRect)


class MenuGameFinish(MenuClass):
    def __init__(self, surface, engine):
        MenuClass.__init__(self, surface)

        self.engine = engine

        self.text = ('GAME COMPLETED\n'
            'Thanks for playing MINER, my PyWeek #17 entry!')

    def draw(self):
        self.surface.fill(self.backgroundColor)

        self.renderText()
        self.drawHint()

        # update surface
        pygame.display.update()

    def _handleEvents(self, event):
        def pressed(key):
            keys = pygame.key.get_pressed()

            if keys[key]:
                return True
            else:
                return False

        if pressed(pygame.K_x):
            self.engine.setState(MENU_STARTGAME)

    def renderText(self):
        # split texts at \n (newline)

        texts = self.text.split('\n')

        for i in range(len(texts)):
            textSurface = self.textFont.render(texts[i], 0, (255, 255, 255))

            textRect = textSurface.get_rect()
            textRect.centerx = SCREEN_WIDTH / 2
            textRect.centery = SCREEN_HEIGHT / 2 + i * self.textFont.size(
                texts[i])[1]

            self.surface.blit(textSurface, textRect)

    def drawHint(self):
        textSurface = self.textFont.render(
            '(Click X to return to main screen)', 0, (255, 255, 255))
        textRect = textSurface.get_rect()
        textRect.centerx = SCREEN_WIDTH / 2
        textRect.centery = SCREEN_HEIGHT - 50
        self.surface.blit(textSurface, textRect)
