from importlib import readers
from src.Settings import*

from src.core.equipment.weapon.Weapon import Weapon
from src.entities.Mob import Mob
import pygame


class Player(Mob):
    def __init__(self, health: int, attack: int, defence: int, movespeed: float, yMovementSpeed: float, image: pygame.Surface, framesPath: str, health_max: int, onGround: bool = True, equipment: list[Weapon] = None):
        super().__init__(health, attack, defence, movespeed, yMovementSpeed, image, framesPath)
        self.onGround = onGround
        self.ySpeed = 0
        self.hearthImage = pygame.image.load(HEARTH_IMAGE).convert_alpha()
        self.dashing = {"isDashing": False, "orientation": "", "timer": 0 ,"canDash": True}
        self.equipment = equipment if equipment is not None else []
        self.health_max = health_max
        self.load_sound("dash", "assets/sound/vfx/dash.mp3", 0.3)
        self.load_sound("punch", "assets/sound/vfx/poingt.mp3", 0.6)

    def update_visuals(self, framesPath, image=None, scale=None):
        super().update_visuals(framesPath, image, scale)
        self.rect.inflate_ip(-self.rect.width // 2, -self.rect.height // 4)

    def move(self, rectCollisions: list[pygame.Rect], events, spriteCollisions: list[pygame.sprite.Sprite]):
        keys = pygame.key.get_pressed()
        
        if getattr(self, 'is_flying', False):
            self.xSpeed = 0
            self.ySpeed = 0
            if keys[PLAYER_CLIMB] or keys[pygame.K_UP]:
                self.ySpeed = -self.movespeed * 2
            if keys[PLAYER_UNCLIMB] or keys[pygame.K_DOWN]:
                self.ySpeed = self.movespeed * 2
            if keys[PLAYER_LEFT] or keys[pygame.K_LEFT]:
                self.xSpeed = -self.movespeed * 2
            if keys[PLAYER_RIGHT] or keys[pygame.K_RIGHT]:
                self.xSpeed = self.movespeed * 2
            self.rect.x += self.xSpeed
            self.rect.y += self.ySpeed
            self.animate()
            return
        
        if not self.dashing["isDashing"]:
            if self.wallJump["wallJumpTimerLeft"] > 0:
                self.wallJump["wallJumpTimerLeft"] -= 1
            elif self.wallJump["wallJumpTimerRight"] > 0:
                self.wallJump["wallJumpTimerRight"] -= 1
            else:
                self.xSpeed = 0
                if keys[PLAYER_LEFT]: 
                    self.xSpeed = -self.movespeed
                    self.dashing["orientation"] = "left"
                if keys[PLAYER_RIGHT]: 
                    self.xSpeed = self.movespeed
                    self.dashing["orientation"] = "right"
            
            if self.onGround:
                self.dashing["canDash"] = True

            self.climbing = False
            if self.climb and keys[PLAYER_CLIMB]:
                self.climbing = True
                self.ySpeed = -self.yMovementSpeed / 5
            elif self.climb and keys[PLAYER_UNCLIMB]:
                self.climbing = True
                self.ySpeed = self.yMovementSpeed / 5

            if keys[PLAYER_JUMP] and (self.onGround or self.climb):
                self.ySpeed = -self.yMovementSpeed
                self.onGround = False

            
        self._dash(events)
        self._jumpLogic(events, keys)
        self._punch(events)

        #COLLISION AND MOOVE
        self.moveAndCollide(rectCollisions, spriteCollisions)


    def _punch(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == PLAYER_PUNCH and not self.is_punching:
                self.is_punching = True
                self.has_punched = False
                self.frame_index = 0
                self.play_sound("punch")

    def _dash(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == PLAYER_DASH and self.dashing["orientation"] != "" and self.dashing["canDash"]:
                self.dashing["isDashing"] = True
                self.dashing["timer"] =  PLAYER_DASH_TIMER
                self.dashing["canDash"] = False
                self.play_sound("dash")

        if self.dashing["isDashing"]:
            if self.dashing["timer"] > 0:
                if self.dashing["orientation"] == "left":
                    self.xSpeed = -PLAYER_DASH_POWER * self.movespeed
                elif self.dashing["orientation"] == "right":
                    self.xSpeed = PLAYER_DASH_POWER * self.movespeed
                self.ySpeed = 0
                self.dashing["timer"] -= 1
                self.dashing["canDash"] = False
            else:
                self.dashing["isDashing"] = False
                self.dashing["orientation"] = ""

    def heal(self):
        self.health += HEALTH_POTION
        if self.health > self.health_max:
            self.health = self.health_max

    def _jumpLogic(self, events, keys):
        self.is_wall_sliding = False
        self.wall_sliding_direction = ""
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == PLAYER_JUMP:
                if self.onGround:
                    self.ySpeed = -self.yMovementSpeed
                    self.onGround = False
                elif self.wallJump["wallJumpTimerLeft"] == 0 and self.wallJump["wallJumpTimerRight"] == 0:
                    if self.wallJump["onWallLeft"]:
                        self.xSpeed = self.movespeed * PLAYER_WALL_JUMP_POWER 
                        self.ySpeed = -self.yMovementSpeed
                        self.wallJump["wallJumpTimerLeft"] = PLAYER_WALL_JUMP_TIMER
                    elif self.wallJump["onWallRight"]:
                        self.xSpeed = -self.movespeed * PLAYER_WALL_JUMP_POWER
                        self.ySpeed = -self.yMovementSpeed
                        self.wallJump["wallJumpTimerRight"] = PLAYER_WALL_JUMP_TIMER

        if self.ySpeed >= 0:
            is_grabbing_wall = (self.wallJump["onWallLeft"] and keys[PLAYER_LEFT]) or (self.wallJump["onWallRight"] and keys[PLAYER_RIGHT])
            if is_grabbing_wall:
                self.is_wall_sliding = True
                self.wall_sliding_direction = "left" if self.wallJump["onWallLeft"] else "right"
                self.dashing["canDash"] = True
                if self.wallJump["wallStabilizeTimer"] > 0:
                    self.ySpeed = -0.5
                    self.wallJump["wallStabilizeTimer"] -= 1
                else:
                    self.ySpeed = 2 
        
    def drawLife(self, screen):
        for i in range(self.health):
            xPos = 20 + (i*40)
            yPos = 20
            screen.blit(self.hearthImage, (xPos, yPos))




