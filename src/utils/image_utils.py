import pygame
import os

def process_surface(img: pygame.Surface, scale: float = 1.0, flip_x: bool = False, crop_bottom: bool = True) -> pygame.Surface:
    
    if crop_bottom:
        bbox = img.get_bounding_rect()
        if bbox.height > 0:
            img = img.subsurface(pygame.Rect(0, 0, img.get_width(), bbox.bottom)).copy()
            
    if scale != 1.0:
        img = pygame.transform.scale_by(img, scale)
        
    if flip_x:
        img = pygame.transform.flip(img, True, False)
        
    return img

def load_image(file_path: str, scale: float = 1.0, flip_x: bool = False, crop_bottom: bool = True) -> pygame.Surface:
    
    img = pygame.image.load(file_path).convert_alpha()
    return process_surface(img, scale, flip_x, crop_bottom)

def load_frames(folder: str, scale: float = 1.0, flip_x: bool = False, crop_bottom: bool = True) -> list[pygame.Surface]:
    
    frames = []
    if os.path.isdir(folder):
        for f in os.listdir(folder):
            file_path = os.path.join(folder, f)
            if os.path.isfile(file_path):
                img = load_image(file_path, scale, flip_x, crop_bottom)
                frames.append(img)
    return frames
