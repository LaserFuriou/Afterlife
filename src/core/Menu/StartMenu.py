import pygame
from src.core.Menu.Menu import Menu
from src.core.Menu.Button import Button
import src.Settings as Settings

class StartMenu(Menu):

    def __init__(self, playerAction, creditsAction, quitAction):
        super().__init__("", (25, 30, 45))
        self.playerAction = playerAction
        self.creditsAction = creditsAction
        self.quitAction = quitAction
        
        try:
            self.bg_image = pygame.image.load("assets/graphics/menu/menuBackground.png").convert_alpha()
            self.bg_image = pygame.transform.scale(self.bg_image, (Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        except Exception as e:
            print(f"Warning: Could not load menuBackground.png: {e}")
            self.bg_image = None
            
        screenW = Settings.SCREEN_WIDTH
        centerX = screenW // 2
        
        btnW, btnH = 240, 60
        btnX = centerX - (btnW // 2)
        
        cNormal = (30, 20, 50)
        cHover = (220, 40, 100)
        
        startY = 480
        gap = 80
        
        self.startButton = Button(btnX, startY, btnW, btnH, "Lancer le Jeu", cNormal, cHover, self.playerAction)
        self.creditsButton = Button(btnX, startY + gap, btnW, btnH, "Crédits", cNormal, cHover, self.creditsAction)
        self.quitButton = Button(btnX, startY + gap * 2, btnW, btnH, "Quitter", cNormal, cHover, self.quitAction)
        
        self.addButton(self.startButton)
        self.addButton(self.creditsButton)
        self.addButton(self.quitButton)

    def drawMenu(self, screen):
        if self.bg_image:
            screen.blit(self.bg_image, (0, 0))
        else:
            screen.fill(self.background)
        
        mousePos = pygame.mouse.get_pos()
        textSurface = self.TITLESET.render(self.title, True, (245, 245, 250))
        textRect = textSurface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4))
        screen.blit(textSurface, textRect)

        for button in self.buttons:
            button.draw(screen, mousePos)

    def launchGame(self):
        print("Launch Game ! Have fun")