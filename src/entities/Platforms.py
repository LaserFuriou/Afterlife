import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])

        self.width = width
        self.height = height

        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

class LinearMovingPlatform(Platform):
    """
    # vx est la vitesse horizontal par frame (avec négatif vers la droite)
    # et vy pour la vitesse verticale (avec négatif vers le haut)
    # length est la distance en absolu totale à parcourir
    # pause est le temps en frames d'arrêt avant de repartir (60 frames par seconde)
    # ATTENTION ne pas faire de diagonale avec vx != vy sinon ça ne marche pas
    """
    def __init__(self, x, y, width, height, vx, vy, length, pause, image, blocking, damaging):
        Platform.__init__(self, x, y, width, height)

        self.image = image

        self.vx = vx
        self.movesX = vx != 0
        self.vy = vy
        self.movesY = vy != 0
        self.length = length

        self.startPause = pause
        self.pause_x = pause
        self.pause_y = pause

        self.blocking = blocking
        self.damaging = damaging
        self.id = "platform"

        self.inPause = False

        self.start_x = x
        self.start_y = y

        if vx >= 0:
            self.end_x=x+length
        else:
            self.end_x=x-length
        if vy >= 0:
            self.end_y=y+length
        else:
            self.end_y=y-length

    def draw(self, surface, offset):
        surface.blit(self.image,(self.rect.x - offset.x,self.rect.y - offset.y))

    def update(self):
        if ((self.vx >= 0 and self.rect.x < self.end_x)
        or (self.vx <= 0 and self.rect.x > self.end_x)):
            self.rect.x += self.vx
        else:
            if self.pause_x != 0:
                self.pause_x -= 1
                self.inPause = True
            else:
                self.inPause = False
                self.vx = -self.vx

                tmpEndX = self.end_x
                self.end_x = self.start_x
                self.start_x = tmpEndX

                self.pause_x = self.startPause

        if ((self.vy >= 0 and self.rect.y < self.end_y)
        or (self.vy <= 0 and self.rect.y > self.end_y)):
            self.rect.y += self.vy
        else:
            if self.pause_y != 0:
                self.pause_y -= 1
            else:
                self.vy = -self.vy

                tmpEndY = self.end_y
                self.end_y = self.start_y
                self.start_y = tmpEndY

                self.pause_y = self.startPause

# TODO : voir comment faire tourner les rectangles avec PyGames
class RotatingMovingPlatform(Platform):
    def __init__(self, x, y, width, height, spd, radius, angle, pause):
        Platform.__init__(self, x, y, width, height)

        self.startPause = pause
        self.pause_x = pause
        self.pause_y = pause

        self.spd = spd
        self.radius = radius
        self.angle = angle

        self.center = (x,y)
