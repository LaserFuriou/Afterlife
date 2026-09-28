from src.entities.Mob import Mob
from src.Settings import SPRITE_SCALE
import pygame
import os


class Npc(Mob):
    def __init__(self, health: int, attack: int, defence: int, movespeed: float, yMovementSpeed: float, image: pygame.Surface, framesPath: str, name: str, onGround: bool = True,):
        super().__init__(health, attack, defence, movespeed, yMovementSpeed, image, framesPath, scale=SPRITE_SCALE * 2)
        self.onGround = onGround
        self.dialog_range = 100
        self.name = name
        self.dialog_number = "0"
        self.dialogPath = "assets/dialogs/" + self.name + "/dialog" + self.dialog_number + ".txt"

    def get_dialog_rect(self):
        return self.rect.inflate(self.dialog_range, self.dialog_range)

    def get_name(self):
        return self.name

    def get_dialog_path(self):
        return self.dialogPath

    def set_dialog_number(self, number: str):
        self.dialog_number = number
        self.dialogPath = "assets/dialogs/" + self.name + "/dialog" + self.dialog_number + ".txt"


    def get_dialog(self, dialog_number: str):
        self.set_dialog_number(dialog_number)
        dialog = "..."
        if os.path.exists(self.dialogPath):
            with open(self.dialogPath, "r") as f:
                dialog = f.read().strip()
        return dialog