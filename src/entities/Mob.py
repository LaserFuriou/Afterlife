import os
from src.entities.Entity import Entity
from src.Settings import *
from src.level import Level
import pygame

from src.utils.image_utils import load_frames, load_image, process_surface

class Mob(Entity):
    def __init__(self, health: int, attack: int, defence: int, movespeed: float, yMovementSpeed: float, image: pygame.Surface, framesPath: str, onGround: bool = True, scale: float = SPRITE_SCALE):
        super().__init__(health, attack, defence, movespeed, yMovementSpeed, image)
        self.scale = scale
        self.ySpeed = 0
        self.xSpeed = 0
        self.wallJump = {"onWallLeft" : False, "onWallRight": False, "wallJumpTimerLeft": 0, "wallJumpTimerRight": 0, "wallStabilizeTimer": 0}
        self.onGround = onGround
        self.z_index = 10 
        self.displaySurface = pygame.display.get_surface()
        self.climb = False
        self.climbing = False
        self.is_wall_sliding = False
        self.wall_sliding_direction = ""
        self.is_shooting = False
        self.shoot_timer = 170
        self.on_shoot_callback = None
        self.has_shot = False
        
        self.is_punching = False
        self.has_punched = False
        self.on_punch_callback = None
        self.facing_direction = "right"
        self.sounds = {}
        self.load_sound("shoot", "assets/sound/vfx/ammo.mp3", 0.3)
        self.update_visuals(framesPath, image, scale=self.scale)

    def load_sound(self, name, filepath, volume=0.3):
        try:
            sound = pygame.mixer.Sound(filepath)
            sound.set_volume(volume)
            self.sounds[name] = sound
        except Exception as e:
            print(f"probleme chargement sond : {name}: {e}")

    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()
    def update_visuals(self, framesPath, image=None, scale=None):
        if scale is None:
            scale = getattr(self, 'scale', SPRITE_SCALE)
        self.framesPath = framesPath
        east_frames = load_frames(framesPath + "/running/", scale)
        east_jump_frames = load_frames(framesPath + "/jumping/", scale)
        shoot_frames = load_frames(framesPath + "/shoot/", scale)
        wall_slide_frames = load_frames(framesPath + "/wall_slide/", scale)
        
        punch_frames = load_frames(framesPath + "/punch/", scale)
        if not punch_frames:
            punch_frames = []

        self.animations = {
            "punch-east": punch_frames,
            "punch-west": [pygame.transform.flip(frame, True, False) for frame in punch_frames],
            "east": east_frames,
            "west": [pygame.transform.flip(frame, True, False) for frame in east_frames],
            "jump-east": east_jump_frames,
            "jump-west": [pygame.transform.flip(frame, True, False) for frame in east_jump_frames],
            "shoot": shoot_frames,
            "wall-slide-left": wall_slide_frames,
            "wall-slide-right": [pygame.transform.flip(frame, True, False) for frame in wall_slide_frames]
        }
        
        self.is_wall_sliding = False
        self.wall_sliding_direction = ""
        
        self.is_shooting = False
        self.shoot_timer = 170
        self.on_shoot_callback = None
        self.has_shot = False

        self.invincible = False
        self.invincibility_timer = 120
        self.invincibility = self.invincibility_timer
        
        files = [f for f in os.listdir(self.framesPath) if os.path.isfile(os.path.join(self.framesPath, f))]
        if files:
            sprite_files = [f for f in files if f.startswith("sprite_")]
            chosen_file = sprite_files[0] if sprite_files else files[0]
            file_path = os.path.join(self.framesPath, chosen_file)
            self.stand_frame = load_image(file_path, scale=scale)
        elif image is not None:
            self.stand_frame = process_surface(image, scale=scale)
        
        self.image = self.stand_frame
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        
        self.frame_index = 0.0
        self.animation_speed = 0.1

    def take_damage(self):
        if not self.invincible:
            self.invincible = True
            self.xSpeed -= 5
            self.ySpeed -= 2
            self.health -= 1

    def is_dead(self, level) -> bool:
        return self.health <= 0 or self.rect.top > level.height * level.tileHeight

    def attack(self):
        return self.attack

    def is_dead(self, level=None) -> bool:
        if level is not None:
            return self.health <= 0 or self.rect.top > level.height * level.tileHeight
        return self.health <= 0

    def moveAndCollide(self, rectCollisions, spriteCollisions):
        self.wallJump["onWallRight"] = False
        self.wallJump["onWallLeft"] = False

        self.image.set_alpha(255)
        if self.invincible:
            print("test")
            self.invincibility -= 1
            if (self.invincibility // 5) % 2 == 0:
                self.image.set_alpha(80)

            if self.invincibility <= 0:
                self.invincible = False
                self.invincibility = self.invincibility_timer

        for wall in spriteCollisions:
            if getattr(wall, "id", None) == "platform" and wall.blocking and not wall.inPause and self.onGround:
                if self.rect.right > wall.rect.left and self.rect.left < wall.rect.right:
                    if self.rect.bottom == wall.rect.top - wall.vy:
                        self.xSpeed += wall.vx
                        self.rect.y += wall.vy
                        break
            if getattr(wall, "id", None) == "laser" and self.rect.colliderect(wall.rect) and wall.live:
                self.take_damage()

        self.rect.x += self.xSpeed
        self.animate()
        for wall in rectCollisions:
            if self.rect.colliderect(wall["rect"]):
                if self.xSpeed > 0:
                    if wall.get("is_wallJumpable") == True:
                        self.wallJump["onWallRight"] = True
                    self.rect.right = wall["rect"].left
                if self.xSpeed < 0:
                    if wall.get("is_wallJumpable") == True:
                        self.wallJump["onWallLeft"] = True
                    self.rect.left = wall["rect"].right

        alreadyChangedSpeed = False
        changed = False
        for wall in spriteCollisions:
            if wall.blocking:
                if self.rect.colliderect(wall.rect):
                    onTop = abs(self.rect.top - wall.rect.top) == abs(self.rect.height + wall.vy)
                    if self.xSpeed > 0 and not onTop:
                        self.rect.right = wall.rect.left
                    if self.xSpeed < 0 and not onTop:
                        self.rect.left = wall.rect.right
            else:
                if getattr(wall, "id", None) != "laser" and not changed:
                    if self.rect.colliderect(wall.rect):
                        self.climb = True
                        changed = True
                    else:
                        self.climb = False


        if not self.climb:
            self.ySpeed += 0.5
        else:
            if not self.climbing:
                self.ySpeed = 0
        self.rect.y += self.ySpeed
        self.onGround = False

        for wall in rectCollisions:
            if self.rect.colliderect(wall["rect"]):
                if self.ySpeed > 0:
                    self.rect.bottom = wall["rect"].top
                    self.ySpeed = 0
                    self.onGround = True
                    self.wallJump["wallStabilizeTimer"] = 20
                elif self.ySpeed < 0:
                    self.rect.top = wall["rect"].bottom
                    self.ySpeed = 0

        for wall in spriteCollisions:
            if self.rect.colliderect(wall.rect) and wall.blocking:
                if self.ySpeed > 0:
                    self.rect.bottom = wall.rect.top
                    self.ySpeed = 0
                    self.onGround = True
                elif self.ySpeed < 0:
                    self.rect.top = wall.rect.bottom
                    self.ySpeed = 0

    def is_on_screen(self):
        for group in self.groups():
            if hasattr(group, 'offset'):
                visible_rect = pygame.Rect(
                    group.offset.x + 256, 
                    group.offset.y + 192, 
                    512, 
                    384
                )
                return self.rect.colliderect(visible_rect)
        return True
    def animate(self):
        old_midbottom = self.rect.midbottom

        if not self.is_shooting:
            if self.is_on_screen():
                self.shoot_timer += 1
                if self.shoot_timer >= 180:
                    self.is_shooting = True
                    self.frame_index = 0
                    self.shoot_timer = 0
                    self.has_shot = False

        if self.is_shooting:
            frames = self.animations["shoot"]
            if frames:
                self.frame_index += self.animation_speed * 2.0
                
                if not self.has_shot and self.frame_index >= len(frames) - 2.0:
                    self.has_shot = True
                    self.play_sound("shoot")
                    if self.on_shoot_callback:
                        self.on_shoot_callback(self)

                if self.frame_index >= len(frames):
                    self.is_shooting = False
                    self.frame_index = 0
                    self.image = self.stand_frame
                else:
                    self.image = frames[int(self.frame_index)]
                self.rect.midbottom = old_midbottom
                return
            else:
                self.is_shooting = False

        if self.xSpeed > 0:
            self.facing_direction = "right"
        elif self.xSpeed < 0:
            self.facing_direction = "left"

        if self.is_punching:
            direction = "punch-east" if self.facing_direction == "right" else "punch-west"
            frames = self.animations.get(direction, [])
            if frames:
                self.frame_index += self.animation_speed * 3.0
                
                if not self.has_punched and self.frame_index >= len(frames) - 1.0:
                    self.has_punched = True
                    if self.on_punch_callback:
                        self.on_punch_callback(self)

                if self.frame_index >= len(frames):
                    self.is_punching = False
                    self.frame_index = 0
                    self.image = self.stand_frame
                else:
                    self.image = frames[int(self.frame_index)]
                self.rect.midbottom = old_midbottom
                return
            else:
                self.is_punching = False

        if self.xSpeed == 0:
            self.image = self.stand_frame
            self.frame_index = 0
            self.rect.midbottom = old_midbottom
            return

        if self.is_wall_sliding:
            direction = "wall-slide-left" if self.wall_sliding_direction == "left" else "wall-slide-right"
        elif self.xSpeed > 0 and self.ySpeed <= 0.5:
            direction = "east"
        elif self.xSpeed < 0 and self.ySpeed <= 0.5:
            direction = "west"
        elif self.xSpeed > 0 and self.ySpeed > 0.5:
            direction = "jump-east"
        elif self.xSpeed < 0 and self.ySpeed > 0.5:
            direction = "jump-west"
        frames = self.animations[direction]

        if not frames:
            self.image = self.stand_frame
            self.rect.midbottom = old_midbottom
            return

        self.frame_index += self.animation_speed
        if self.frame_index >= len(frames):
            self.frame_index = 0

        self.image = frames[int(self.frame_index)]
        self.rect.midbottom = old_midbottom
