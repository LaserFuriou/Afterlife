import pygame
from src.core.Menu.Menu import Menu
from src.core.Menu.Button import Button
import src.Settings as Settings

class PauseMenu(Menu):

    def __init__(self, playerAction, creditsAction, quitAction):
        super().__init__("PAUSE", (0, 0, 0, 128))
        self.playerAction = playerAction
        self.creditsAction = creditsAction
        self.quitAction = quitAction
        
        screenW = Settings.SCREEN_WIDTH
        centerX = screenW // 2
        
        btnW, btnH = 240, 60
        btnX = centerX - (btnW // 2)
        
        cNormal = (30, 20, 50)
        cHover = (220, 40, 100)
        
        startY = 480
        gap = 80
        
        self.startButton = Button(btnX, startY, btnW, btnH, "Reprendre", cNormal, cHover, self.playerAction)
        self.creditsButton = Button(btnX, startY + gap, btnW, btnH, "Crédits", cNormal, cHover, self.creditsAction)
        self.quitButton = Button(btnX, startY + gap * 2, btnW, btnH, "Quitter", cNormal, cHover, self.quitAction)
        
        self.addButton(self.startButton)
        self.addButton(self.creditsButton)
        self.addButton(self.quitButton)

    def drawMenu(self, screen):
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill(self.background)
        screen.blit(overlay, (0, 0))
        
        mousePos = pygame.mouse.get_pos()
        textSurface = self.TITLESET.render(self.title, True, (220, 40, 100))
        textRect = textSurface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4))
        screen.blit(textSurface, textRect)

        for button in self.buttons:
            button.draw(screen, mousePos)
