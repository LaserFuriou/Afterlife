import pygame
pygame.init()

import src.core.Game as Game
import src.level.Level as Level
import src.entities.Player as Player
import src.Settings as Settings
import src.entities.Npc as Npc

pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))

active_map = Settings.LEVEL_1_MAP_JOUR
level = Level.Level(active_map)

is_day_map = "jour" in active_map.lower() or "day" in active_map.lower() or "cave" in active_map.lower()

if is_day_map:
    player_image_path = "assets/graphics/player/day/sprite_player_day.png"
    player_frames_path = "assets/graphics/player/day"
else:
    player_image_path = "assets/graphics/player/night/sprite_player_night.png"
    player_frames_path = "assets/graphics/player/night"

player_surface = pygame.image.load(player_image_path).convert_alpha()
player = Player.Player(3, 100, 10, 3, 10, player_surface, player_frames_path, 10)
player.rect.bottomleft = level.spawnCoordonate


npcs = {}

game = Game.Game(level, player, npcs)
game.run()
