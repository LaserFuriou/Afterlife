import pygame
from pytmx.util_pygame import handle_transformation

class AnimatedTile(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, frames_data: list, tmx_data, flags=None):
        super().__init__()
        self.frames = []
        
        for frame in frames_data:
            gid = getattr(frame, 'gid', None)
            if gid is None and isinstance(frame, dict):
                gid = frame.get('gid')
                
            duration = getattr(frame, 'duration', None)
            if duration is None and isinstance(frame, dict):
                duration = frame.get('duration')
                
            if gid is not None:
                image = tmx_data.get_tile_image_by_gid(gid)
                if image:
                    if flags:
                        image = handle_transformation(image, flags)
                    self.frames.append({"image": image, "duration": duration or 100})
                
        self.current_frame_index = 0
        self.image = self.frames[0]["image"] if self.frames else pygame.Surface((32, 32))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.z_index = 5
        
        self.last_update = pygame.time.get_ticks()
        
    def update(self):
        if not self.frames:
            return
            
        current_time = pygame.time.get_ticks()
        current_frame = self.frames[self.current_frame_index]
        
        if current_time - self.last_update > current_frame["duration"]:
            self.last_update = current_time
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
            self.image = self.frames[self.current_frame_index]["image"]
