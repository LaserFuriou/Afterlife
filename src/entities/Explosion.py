import pygame
import os
from src.Settings import SPRITE_SCALE
from src.utils.image_utils import load_frames

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, folder: str = "assets/graphics/enemy/explosion"):
        super().__init__()
        
        self.frames = load_frames(folder, SPRITE_SCALE * 1.5)
        self.frame_index = 0
        self.animation_speed = 0.3
        self.z_index = 15
        
        if self.frames:
            self.image = self.frames[0]
        else:
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 100, 0))
            
        self.rect = self.image.get_rect(center=(x, y))
        
    def update(self):
        if self.frames:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.frames):
                self.kill()
            else:
                old_center = self.rect.center
                self.image = self.frames[int(self.frame_index)]
                self.rect = self.image.get_rect(center=old_center)
        else:
            self.kill()
