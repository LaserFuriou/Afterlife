import pygame
import os
from src.Settings import SPRITE_SCALE

from src.utils.image_utils import load_frames

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, bullet_folder: str, hit_folder: str):
        super().__init__()
        
        self.flying_frames = load_frames(bullet_folder, SPRITE_SCALE * 2.0, flip_x=True)
        self.hit_frames = load_frames(hit_folder, SPRITE_SCALE * 2.0, flip_x=True)
        
        self.frame_index = 0
        self.animation_speed = 0.2
        
        if self.flying_frames:
            self.image = self.flying_frames[0]
        else:
            self.image = pygame.Surface((10, 10))
            self.image.fill((255, 0, 0))
            
        self.rect = self.image.get_rect(center=(x, y))
        
        self.vx = -5
        self.distance_travelled = 0
        self.max_distance = 400
        
        self.state = "FLYING"
        
    def moveAndCollide(self, walls, player_rect):
        hit_player = False
        if self.state == "FLYING":
            self.rect.x += self.vx
            self.distance_travelled += abs(self.vx)
            
            if self.flying_frames:
                self.frame_index += self.animation_speed
                if self.frame_index >= len(self.flying_frames):
                    self.frame_index = 0
                old_center = self.rect.center
                self.image = self.flying_frames[int(self.frame_index)]
                self.rect = self.image.get_rect(center=old_center)
                
            collided = False
            for wall in walls:
                if self.rect.colliderect(wall["rect"]):
                    collided = True
                    break
                    
            if self.rect.colliderect(player_rect):
                hit_player = True
                
            if collided or hit_player or self.distance_travelled >= self.max_distance:
                self.state = "HIT"
                self.frame_index = 0
                
        elif self.state == "HIT":
            if self.hit_frames:
                self.frame_index += self.animation_speed
                if self.frame_index >= len(self.hit_frames):
                    self.kill() 
                else:
                    old_center = self.rect.center
                    self.image = self.hit_frames[int(self.frame_index)]
                    self.rect = self.image.get_rect(center=old_center)
            else:
                self.kill()

        return hit_player
