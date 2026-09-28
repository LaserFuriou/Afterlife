from src.core.Menu.Button import Button
import pygame
from src.Settings import*
class Menu():

    def __init__(self, title, background):
        self.buttons = []
        self.title = title
        self.TITLESET = TITLE_FONT
        self.background = background

    def addButton(self, button: Button):
        self.buttons.append(button)

    def addButtons(self, buttons: list):
        self.buttons += buttons

    def drawMenu(self, screen):
        mousePos = pygame.mouse.get_pos()
        screen.fill(self.background)
        textSurface = self.TITLESET.render(self.title, True, (245, 245, 250))
        textRect = textSurface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4))
        screen.blit(textSurface, textRect)

        for button in self.buttons:
            button.draw(screen, mousePos)

    def HandleEvents(self, events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                for b in self.buttons:
                    if b.checkClick(mousePos):
                        b.onClick()
            


        