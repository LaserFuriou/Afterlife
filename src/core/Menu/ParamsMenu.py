import pygame
from src.core.Menu.Menu import Menu
from src.core.Menu.Button import Button
import src.Settings as Settings

class ParamsMenu(Menu):

    def __init__(self, backAction):
        super().__init__("PARAMÈTRES", (25, 30, 45))
        self.backAction = backAction
        
        screenW = Settings.SCREEN_WIDTH
        centerX = screenW // 2
        
        btnW, btnH = 240, 60
        btnX = centerX - (btnW // 2)
        
        cNormal = (50, 90, 200)
        cHover = (70, 120, 240)
        
        self.backButton = Button(btnX, 620, btnW, btnH, "Retour", cNormal, cHover, self.backAction)
        
        self.addButton(self.backButton)

    def drawMenu(self, screen):
        super().drawMenu(screen)
        font = Settings.GAME_FONT
        startY = 250
        
        options = [
            "Volume Musique : 100%",
            "Volume SFX : 100%",
        ]
        
        for i, line in enumerate(options):
            textSurface = font.render(line, True, (245, 245, 250))
            textRect = textSurface.get_rect(center=(screen.get_width() // 2, startY + i * 50))
            screen.blit(textSurface, textRect)
