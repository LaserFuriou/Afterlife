import pygame
from src.core.Menu.Menu import Menu
from src.core.Menu.Button import Button
import src.Settings as Settings

class CreditsMenu(Menu):

    def __init__(self, backAction):
        super().__init__("", (25, 30, 45))
        self.backAction = backAction
        
        screenW = Settings.SCREEN_WIDTH
        centerX = screenW // 2
        
        self.creditsLines = [
            ("Développeurs", "Yann Herbrech, Nolhan Gardais, Quentin Lang"),
            ("Level Design", "Octave Lejeune & Mathieu Daniel"),
            ("Tileset Niveau 1", "Octave Lejeune & Mathieu Daniel"),
            ("Tileset Niveau 2 & Grotte", "Ansi Muz (itch.io)"),
            ("Niveau 3", "itch.io"),
            ("Musiques", "H01Beatz"),
            ("VFX", "pixabay.com"),
            ("Personnages & Animations", "pixelLab"),
            ("Code & Documentation", "Gemini, Claude, ChatGPT")
        ]
        
        btnW, btnH = 240, 60
        btnX = centerX - (btnW // 2)
        
        cNormal = (50, 90, 200)
        cHover = (70, 120, 240)
        
        self.backButton = Button(btnX, 640, btnW, btnH, "Retour", cNormal, cHover, self.backAction)
        
        self.addButton(self.backButton)

    def drawMenu(self, screen):
        super().drawMenu(screen)
        
        font = Settings.GAME_FONT
        startY = 180
        line_spacing = 45
        
        for i, (role, names) in enumerate(self.creditsLines):
            role_surf = font.render(role + " :", True, (100, 200, 255))
            role_rect = role_surf.get_rect(right=screen.get_width() // 2 - 15, top=startY + i * line_spacing)
            screen.blit(role_surf, role_rect)
            
            name_surf = font.render(names, True, (230, 230, 235))
            name_rect = name_surf.get_rect(left=screen.get_width() // 2 + 15, top=startY + i * line_spacing)
            screen.blit(name_surf, name_rect)
