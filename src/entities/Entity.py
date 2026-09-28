import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, health: int, attack: int, defence: int, movespeed: float, yMovementSpeed: float, image: pygame.Surface):
        super().__init__()
        self.health = health
        self.attack = attack
        self.defence = defence
        self.movespeed = movespeed
        self.yMovementSpeed = yMovementSpeed
        self.image = image
        self.rect = self.image.get_rect()
        self.z_index = 10

    def can_take_damage(self) -> bool:
        return self.defence >= 0

    def set_unbreakable(self) -> None:
        self.defence = -1

    def can_move(self) -> bool:
        return self.movespeed >= 0

    def set_not_moveable(self) -> None:
        self.movespeed = -1