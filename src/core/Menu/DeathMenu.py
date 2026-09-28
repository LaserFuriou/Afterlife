import pygame
from src.core.Menu.Menu import Menu
from src.core.Menu.Button import Button
import src.Settings as Settings

class DeathMenu(Menu):

    def __init__(self, respawnAction, quitAction):
        super().__init__("MORT", (50, 0, 0, 180))
        self.respawnAction = respawnAction
        self.quitAction = quitAction
        
        screenW = Settings.SCREEN_WIDTH
        centerX = screenW // 2
        
        btnW, btnH = 260, 60
        btnX = centerX - (btnW // 2)
        
        cNormal = (150, 30, 30)
        cHover = (200, 50, 50)
        
        self.respawnButton = Button(btnX, 350, btnW, btnH, "Réapparaître", cNormal, cHover, self.respawnAction)
        self.quitButton = Button(btnX, 450, btnW, btnH, "Quitter", cNormal, cHover, self.quitAction)
        
        self.addButton(self.respawnButton)
        self.addButton(self.quitButton)

    def drawMenu(self, screen):
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill(self.background)
        screen.blit(overlay, (0, 0))
        
        mousePos = pygame.mouse.get_pos()
        textSurface = self.TITLESET.render(self.title, True, (255, 100, 100))
        textRect = textSurface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4))
        screen.blit(textSurface, textRect)

        for button in self.buttons:
            button.draw(screen, mousePos)
