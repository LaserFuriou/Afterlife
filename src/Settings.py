import pygame

# --- WINDOW & FPS ---
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
GAME_FONT = pygame.font.Font(None, 30)
TITLE_FONT = pygame.font.Font(None, 40)
COLOR_TEXT = pygame.Color(64, 64, 64)

LEVEL_O_MAP_FILEPATH = "src/level/level_0/test-2d.tmx"
LEVEL_1_MAP_JOUR = "src/level/LVL1-JOUR/MAP_STAGE_1.tmx"
LEVEL_1_MAP_NUIT = "src/level/LVL1-NUIT/MAP_STAGE_1 - NUIT.tmx"
LEVEL_1_MAP_CAVE = "src/level/LVL1-CAVE/cave_STAGE_1.tmx"
LEVEL_2_JOUR_MAP_FILEPATH = "src/level/level2-Jour/level2.tmx"
LEVEL_2_MAP_NUIT = "src/level/level2-nuit/level2-Night.tmx"
LEVEL_3_MAP_AFTERLIGHT = "src/level/AFTERLIGHT/stage3.tmx"
# --- PLAYER ---
HEALTH_POTION = 3
MAX_LINES = 3
HEARTH_IMAGE = "assets/graphics/player/hearth/hearth.png"

# -- PLAYER PARAM --
PLAYER_LEFT = pygame.K_q
PLAYER_RIGHT = pygame.K_d
PLAYER_JUMP = pygame.K_SPACE
PLAYER_INTERACTION = pygame.K_e
PLAYER_PUNCH = 1
PLAYER_DASH = pygame.K_LSHIFT
PLAYER_CLIMB = pygame.K_z
PLAYER_UNCLIMB = pygame.K_s
PLAYER_DASH_TIMER = 12
PLAYER_DASH_POWER = 2

SPRITE_SCALE = 0.55

PLAYER_WALL_JUMP_TIMER = 15
PLAYER_WALL_JUMP_POWER = 1.25