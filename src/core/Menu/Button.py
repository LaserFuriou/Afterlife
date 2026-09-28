from src.Settings import*
import pygame

class Button():
    def __init__(self, posX, posY, width, height, text, color, colorHover, action):
        self.buttonRect = pygame.Rect(posX, posY, width, height)
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.colorHover = colorHover
        self.FONT = GAME_FONT
        self.COLORTEXT = COLOR_TEXT
        self.action = action

    def draw(self,screen,mousePos):
        radius = self.height // 2
        if self.checkClick(mousePos):
            pygame.draw.rect(screen, self.colorHover, self.buttonRect, border_radius=radius) 
        else:
            pygame.draw.rect(screen, self.color, self.buttonRect, border_radius=radius)
            
        

        textSurface = self.FONT.render(self.text, True, (245, 245, 250))
        textRect = textSurface.get_rect(center=self.buttonRect.center)
        screen.blit(textSurface, textRect)
            
    def checkClick(self, mousePos):
        return self.buttonRect.collidepoint(mousePos)

    def onClick(self):
        self.action()
