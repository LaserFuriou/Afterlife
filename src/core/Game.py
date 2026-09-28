from src.core.Menu.CreditsMenu import CreditsMenu
from src.core.Menu.StartMenu import StartMenu
from src.core.Menu.PauseMenu import PauseMenu
from src.core.Menu.DeathMenu import DeathMenu
import pygame
import src.Settings as Settings
from src.core.dialogs.DialogBox import DialogBox
from src.entities.Npc import Npc
from src.entities.Mob import Mob
from src.level import Level
from src.entities.Player import Player
from src.core.Camera.Camera import Camera
from src.entities.Projectile import Projectile
import os
from src.entities.Mob import Mob
from src.entities.Explosion import Explosion

class Game:
    def __init__(self, level: Level, player: Player, noPlayableCharacters: list[Npc]):
        self.level = level
        self.player = player
        self.enemies = []
        self.noPlayableCharacters = noPlayableCharacters
        self.screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.camera = Camera()
        self.playerGroup = pygame.sprite.Group()
        self.enemiesGroup = pygame.sprite.Group()
        self.npcGroup = pygame.sprite.Group()
        self.projectilesGroup = pygame.sprite.Group()

        self.startMenu = StartMenu(self.goGame, self.goCredits, self.quitGame)
        self.creditsMenu = CreditsMenu(self.goStartMenu)
        self.pauseMenu = PauseMenu(self.goGame, self.goCredits, self.quitGame)
        self.deathMenu = DeathMenu(self.respawnPlayer, self.quitGame)
        self.currentMenu = self.startMenu
        self.gameStarted = False
        
        if self.level.filepath == Settings.LEVEL_1_MAP_NUIT:
            self.currLvl = "Level1N"
        elif self.level.filepath == Settings.LEVEL_1_MAP_CAVE:
            self.currLvl = "Level1Cave"
        elif self.level.filepath == Settings.LEVEL_2_JOUR_MAP_FILEPATH:
            self.currLvl = "Level2J"
        elif self.level.filepath == Settings.LEVEL_2_MAP_NUIT:
            self.currLvl = "Level2N"
        else:
            self.currLvl = "Level1J"

        self.player.on_punch_callback = self.handle_punch

        self.playerGroup.add(self.player)
        self._spawn_enemies_from_level()
        self._spawn_npcs_from_level()
        for npc in self.noPlayableCharacters:
            self.npcGroup.add(npc)
            self.camera.add(npc)
        self.camera.add(self.player)

        self.dialog_box = DialogBox(self.screen)
        self.font = pygame.font.Font(None, 36)
        self.printAction = False

        self.camera.add(self.level.collisionSprites)
        if hasattr(self.level, 'animatedSprites'):
            self.camera.add(self.level.animatedSprites)
        
        self.isInMenu = True

    def play_music(self):
        try:
            target_music = "assets/sound/music/HappyAndLessHappyLoop.ogg"
                
            if getattr(self, 'current_music', None) != target_music:
                self.current_music = target_music
                pygame.mixer.music.load(target_music)
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1, 0.0)
        except Exception as e:
            print("probleme(s) avec musicque", e)

    def run(self):
        self.running = True
        while self.running:
            self.screen.fill((128, 128, 128))
            events = pygame.event.get()
            for event in events:
                npc = self.is_player_near()
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == Settings.PLAYER_INTERACTION and not self.dialog_box.visible:
                        if npc is not None:
                            self.dialog_box.show(npc.get_dialog("1"), npc_name= npc.get_name())
                    elif event.key == Settings.PLAYER_INTERACTION:
                        if self.dialog_box.visible:
                            self.dialog_box.next_page()
                        else:
                            self.dialog_box.hide()

            self.menuSelect(events)
            if self.gameStarted:
                self.player.drawLife(self.screen)
            pygame.display.flip()
            self.clock.tick(Settings.FPS)

    def menuSelect(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.isInMenu:
                        # Peut pas leave le mode mort
                        if self.currentMenu != self.deathMenu:
                            self.isInMenu = False
                    else:
                        if self.gameStarted:
                            self.currentMenu = self.pauseMenu
                        self.isInMenu = True

        if self.isInMenu:
            if self.gameStarted:
                self.camera.customDraw(self.player, self.level)
            self.inMenuTime(events)
        else:
            self.inLevelTime(events)

        if self.dialog_box.visible:
            self.dialog_box.draw()

    def inMenuTime(self, events):
        self.currentMenu.drawMenu(self.screen)
        self.currentMenu.HandleEvents(events)


    def inLevelTime(self, events):
        
        if self.player.is_dead(self.level): 
            self.player.health = 0
            self.currentMenu = self.deathMenu
            self.isInMenu = True
            return

        if not self.dialog_box.visible:
            self.handleCheats(events)
            self.player.move(self.level.getCollisionRects(), events, self.level.collisionSprites)
            for enemy in self.enemies:
                enemy.moveAndCollide(self.level.getCollisionRects(), self.level.collisionSprites)
            for npc in self.noPlayableCharacters:
                npc.moveAndCollide(self.level.getCollisionRects(), self.level.collisionSprites)
            for proj in self.projectilesGroup:
                if proj.moveAndCollide(self.level.getCollisionRects(), self.player.rect):
                    self.player.take_damage()
        self.camera.update()

        show_teleport_text = self.changeLvl(events)
        self.camera.customDraw(self.player, self.level)
        if self.printAction:
            text = self.font.render("(E) Discuter", True, "white")
            positionText = text.get_rect()
            positionText.center = (self.screen.get_width() /2, self.screen.get_height() - 40)
            self.screen.blit(text, positionText)
        
        if show_teleport_text:
            self.draw_teleport_text()

    def draw_teleport_text(self):
        if not hasattr(self, 'font'):
            self.font = pygame.font.SysFont("arial", 20, bold=True)
        texte = self.font.render("Appuyez sur E pour accéder !", True, (255, 255, 255))
        
        bg_surf = pygame.Surface((texte.get_width() + 10, texte.get_height() + 4))
        bg_surf.set_alpha(150)
        bg_surf.fill((0, 0, 0))
        
        pos_x = self.player.rect.centerx - self.camera.offset.x - bg_surf.get_width()//2
        pos_y = self.player.rect.top - self.camera.offset.y - 40
        
        self.screen.blit(bg_surf, (pos_x, pos_y))
        self.screen.blit(texte, (pos_x + 5, pos_y + 2))

    def changeLvl(self, events):
        for lvl_obj in self.level.changeLvlRects:
            if self.player.rect.colliderect(lvl_obj["rect"]):
                target_name = lvl_obj["name"]
                trigger = lvl_obj.get("autoTP", False)
                if not trigger:
                    for event in events:
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                            trigger = True
                            break

                if trigger:
                    self.camera.remove(self.level.collisionSprites)
                    if hasattr(self.level, 'animatedSprites'):
                        self.camera.remove(self.level.animatedSprites)
                        
                    targetName = lvl_obj["name"]

                    if self.currLvl == "Level1J":
                        # Permet la gestion de la groote dans le niveau 1 jour
                        if targetName == "goGrotte":
                            self.level = Level.Level(Settings.LEVEL_1_MAP_CAVE)
                            self.currLvl = "Level1Cave"
                        else:
                            self.level = Level.Level(Settings.LEVEL_1_MAP_NUIT)
                            self.currLvl = "Level1N"
                    elif self.currLvl == "Level1Cave":
                        self.level = Level.Level(Settings.LEVEL_1_MAP_JOUR)
                        if len(self.level.spawnPoints) > 1:
                            self.level.spawnCoordonate = self.level.spawnPoints[1]
                            self.player.climb = False
                            self.player.climbing = False
                        self.currLvl = "Level1J"
                    elif self.currLvl == "Level2J":
                        self.level = Level.Level(Settings.LEVEL_2_MAP_NUIT)
                        self.currLvl = "Level2N"
                    elif self.currLvl == "Level2N":
                        self.level = Level.Level(Settings.LEVEL_3_MAP_AFTERLIGHT)
                        self.currLvl = "Level3J"
                    elif self.currLvl == "Level1N":
                        self.level = Level.Level(Settings.LEVEL_2_JOUR_MAP_FILEPATH)
                        self.currLvl = "Level2J"
                    
                
                    self.camera.add(self.level.collisionSprites)
                    if hasattr(self.level, 'animatedSprites'):
                        self.camera.add(self.level.animatedSprites)
                    self.respawnPlayer()
                    self.camera.recenter(self.player)

                    self.play_music()
                    return False
                return True
        return False

    def _spawn_enemies_from_level(self):
        for enemy in self.enemies.copy():
            self.enemiesGroup.remove(enemy)
            self.camera.remove(enemy)
            enemy.kill()
        self.enemies = []
        
        for e_data in self.level.enemies_data:
            folder = f"assets/graphics/enemy/paladin/{e_data['type']}"
            surface = pygame.image.load(f"{folder}/rotations/west.png").convert_alpha()
            mob = Mob(100, 100, 10, 10, 10, surface, folder)
            mob.rect.x = e_data["x"]
            mob.rect.y = e_data["y"]
            mob.on_shoot_callback = self.spawn_projectile
            self.enemies.append(mob)
            self.enemiesGroup.add(mob)
            self.camera.add(mob)

    def _spawn_npcs_from_level(self):
        for npc in self.noPlayableCharacters.copy():
            self.npcGroup.remove(npc)
            self.camera.remove(npc)
            npc.kill()
        self.noPlayableCharacters = []

        for e_data in self.level.npcs_data:
            folder = f"assets/graphics/npc/AX-400/{e_data['type']}"
            surface = pygame.image.load(f"{folder}/AX-400.png").convert_alpha()
            npc = Npc(100, 100, 10, 10, 10, surface, folder, f"{e_data['name']}")
            npc.rect.x = e_data["x"]
            npc.rect.y = e_data["y"]
            self.noPlayableCharacters.append(npc)
            self.npcGroup.add(npc)
            self.camera.add(npc)

    def handle_punch(self, player):
        punch_rect = player.rect.copy()
        punch_rect.width *= 2
        if player.facing_direction == "left":
            punch_rect.x -= player.rect.width
            
        for enemy in self.enemies.copy():
            if punch_rect.colliderect(enemy.rect):
                enemy.health = 0
                enemy.take_damage()
                
                explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
                self.camera.add(explosion)
                
                self.enemies.remove(enemy)
                self.enemiesGroup.remove(enemy)
                self.camera.remove(enemy)
                enemy.kill()

    def spawn_projectile(self, mob):
        bullet_folder = os.path.join(mob.framesPath, "bullet")
        hit_folder = os.path.join(mob.framesPath, "bullet_hit")
        proj = Projectile(mob.rect.centerx, mob.rect.centery, bullet_folder, hit_folder)
        self.projectilesGroup.add(proj)
        self.camera.add(proj)

    def goGame(self):
        self.gameStarted = True
        self.isInMenu = False
        self.play_music()
        
    def respawnPlayer(self):
        self.player.health = 3 
        
        filepath_lower = self.level.filepath.lower()
        is_day_map = "jour" in filepath_lower or "day" in filepath_lower or "cave" in filepath_lower
        
        if is_day_map:
            player_image_path = "assets/graphics/player/day/sprite_player_day.png"
            player_frames_path = "assets/graphics/player/day"
        else:
            player_image_path = "assets/graphics/player/night/sprite_player_night.png"
            player_frames_path = "assets/graphics/player/night"
            
        player_surface = pygame.image.load(player_image_path).convert_alpha()
        self.player.update_visuals(player_frames_path, player_surface)
        
        self.player.rect.bottomleft = self.level.spawnCoordonate
        self.playerGroup.add(self.player)
        self.camera.add(self.player)
        self.camera.recenter(self.player)
        self.player.xSpeed = 0
        self.player.ySpeed = 0
        self._spawn_enemies_from_level()
        self._spawn_npcs_from_level()
        self.isInMenu = False

    def goCredits(self):
        self.currentMenu = self.creditsMenu

    def goStartMenu(self):
        if self.gameStarted:
            self.currentMenu = self.pauseMenu
        else:
            self.currentMenu = self.startMenu

    def quitGame(self):
        self.running = False

    def is_player_near(self) -> Npc:
        for npc in self.noPlayableCharacters:
            if npc.get_dialog_rect().colliderect(self.player.rect):
                self.printAction = True
                return npc
            else:
                self.printAction = False
        return None

    def handleCheats(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    self.cheat_teleport_to(Settings.LEVEL_1_MAP_JOUR, "Level1J")
                elif event.key == pygame.K_F2:
                    self.cheat_teleport_to(Settings.LEVEL_1_MAP_NUIT, "Level1N")
                elif event.key == pygame.K_F3:
                    self.cheat_teleport_to(Settings.LEVEL_1_MAP_CAVE, "Level1Cave")
                elif event.key == pygame.K_F4:
                    self.cheat_teleport_to(Settings.LEVEL_2_JOUR_MAP_FILEPATH, "Level2J")
                elif event.key == pygame.K_F5:
                    self.cheat_teleport_to(Settings.LEVEL_2_MAP_NUIT, "Level2N")
                elif event.key == pygame.K_F6:
                    self.cheat_teleport_to(Settings.LEVEL_3_MAP_AFTERLIGHT, "Level3J")
                elif event.key == pygame.K_F8:
                    self.player.is_flying = not getattr(self.player, 'is_flying', False)

    def cheat_teleport_to(self, filepath, lvl_name):
        self.camera.remove(self.level.collisionSprites)
        if hasattr(self.level, 'animatedSprites'):
            self.camera.remove(self.level.animatedSprites)
            
        self.level = Level.Level(filepath)
        self.currLvl = lvl_name
        
        self.camera.add(self.level.collisionSprites)
        if hasattr(self.level, 'animatedSprites'):
            self.camera.add(self.level.animatedSprites)
            
        self.respawnPlayer()
        self.camera.recenter(self.player)
        self.play_music()