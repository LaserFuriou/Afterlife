import src.core.Game as Game
import src.level.Level as Level
import src.entities.Player as Player
import src.Settings as Settings
import src.entities.Mob as Mob

import pygame
pygame.init()

pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))

level = Level.Level(Settings.LEVEL_1_MAP_FILEPATH)
player_surface = pygame.image.load("test/assets/graphics/ennemy/knight/rotations/south.png").convert_alpha()
enemy_surface = pygame.image.load("test/assets/graphics/ennemy/knight/rotations/south.png").convert_alpha()
player = Player.Player(100, 100, 10, 3, 10, player_surface,"test/assets/graphics/ennemy/knight", 10)
enemy = Mob.Mob(100, 100, 10, 10, 10, enemy_surface, "test/assets/graphics/ennemy/knight")

game = Game.Game(level, player, enemy)
game.run()