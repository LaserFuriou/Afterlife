from src.level.Level import Level
from src.Settings import *
import pygame

class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        
        self.zoom_scale = 2
        self.internal_surf_size = self.displaySurface.get_size()
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)

        # camera offset
        self.offset = pygame.math.Vector2()
        self.halfW = self.displaySurface.get_size()[0] // 2
        self.halfH = self.displaySurface.get_size()[1] // 2

        # box setup
        self.cameraBorders = {'left': 450, 'right': 450, 'top': 250, 'bottom': 250}
        l = self.cameraBorders['left']
        t = self.cameraBorders['top']
        w = self.displaySurface.get_size()[0] - (self.cameraBorders['left'] + self.cameraBorders['right'])
        h = self.displaySurface.get_size()[1] - (self.cameraBorders['top'] + self.cameraBorders['bottom'])
        self.cameraRect = pygame.Rect(l, t, w, h)

    def boxTargetCamera(self, target):

        if target.rect.left < self.cameraRect.left:
            self.cameraRect.left = target.rect.left
        if target.rect.right > self.cameraRect.right:
            self.cameraRect.right = target.rect.right
        if target.rect.top < self.cameraRect.top:
            self.cameraRect.top = target.rect.top
        if target.rect.bottom > self.cameraRect.bottom:
            self.cameraRect.bottom = target.rect.bottom

        self.offset.x = self.cameraRect.left - self.cameraBorders['left']
        self.offset.y = self.cameraRect.top - self.cameraBorders['top']

    def customDraw(self, player, level):

        self.boxTargetCamera(player)
        largeur_carte = level.width * level.tileWidth
        hauteur_carte = level.height * level.tileHeight
        if self.offset.x < -256:
            self.offset.x = -256
        if self.offset.x > largeur_carte - SCREEN_WIDTH + 256:
            self.offset.x = largeur_carte - SCREEN_WIDTH + 256

        if self.offset.y < -192:
            self.offset.y = -192
        if self.offset.y > hauteur_carte - SCREEN_HEIGHT + 192:
            self.offset.y = hauteur_carte - SCREEN_HEIGHT + 192
        
        self.internal_surf.fill((128, 128, 128))
        
        level.drawMap(self.internal_surf, self.offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: getattr(sprite, 'z_index', 0)):
            display_rect = sprite.image.get_rect(midbottom=sprite.rect.midbottom)
            offsetPos = display_rect.topleft - self.offset
            self.internal_surf.blit(sprite.image, offsetPos)
            
        scaled_surf = pygame.transform.scale_by(self.internal_surf, self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center=(self.halfW, self.halfH))
        
        self.displaySurface.blit(scaled_surf, scaled_rect)

    def recenter(self, target):
        self.cameraRect.left = self.cameraBorders['left']
        self.cameraRect.top = self.cameraBorders['top']
        self.boxTargetCamera(target)