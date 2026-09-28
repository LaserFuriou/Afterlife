import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, pause):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = pygame.Rect(x, y, width, height)
        self.blocking = False
        self.id = "laser"
        self.rect = pygame.Rect(x, y, width, height)
        self.init_pause = pause
        self.pause = pause
        self.live = True
        self.last_switch = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()

        if now - self.last_switch >= self.pause:
            flips = (now - self.last_switch) // self.pause
            if flips % 2 == 1:
                self.live = not self.live
            self.last_switch += flips * self.pause
        self.image.fill((0, 0, 0, 0)) 
        if self.live:
            self.image.fill((255, 0, 0, 180))