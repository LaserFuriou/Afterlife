import pygame
from src.entities.Platforms import *
from src.entities.AnimatedTile import AnimatedTile
from pytmx.util_pygame import load_pygame
import pytmx.util_pygame
from src.entities.Lasers import *

class Level:

    def __init__(self ,filepath):
        self.filepath = filepath
        self.tmxData = load_pygame(filepath)
        self.width = self.tmxData.width
        self.height = self.tmxData.height
        self.tileWidth = self.tmxData.tilewidth
        self.tileHeight = self.tmxData.tileheight
        self.spawnPoints = self._loadSpawnPoints()
        self.spawnCoordonate = self.spawnPoints[0] if self.spawnPoints else (0, 0)
        self.collisionRects = self._loadCollisionRects()
        self.collisionSprites = self._loadCollisionSprites()
        self.changeLvlRects = self._loadChangeLvlRects()
        self.enemies_data = self._loadEnemies()
        self.npcs_data = self._loadNpcs()
        self.animatedSprites = self._loadAnimatedTiles()

    def _loadAnimatedTiles(self):
        animated_sprites = []
        for layer in self.tmxData.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    gid = layer.data[y][x]
                    props = self.tmxData.get_tile_properties_by_gid(gid)
                    if props and 'frames' in props:
                        flags = None
                        tiled_gid = self.tmxData.tiledgidmap.get(gid)
                        if tiled_gid is not None:
                            for g, f in self.tmxData.gidmap.get(tiled_gid, []):
                                if g == gid:
                                    flags = f
                                    break
                                    
                        real_x = x * self.tileWidth
                        real_y = y * self.tileHeight
                        anim_tile = AnimatedTile(real_x, real_y, props['frames'], self.tmxData, flags)
                        animated_sprites.append(anim_tile)
        return animated_sprites

    def _loadEnemies(self):
        enemies = []
        for obj_group in self.tmxData.objectgroups:
            if obj_group.name == "enemies":
                for obj in obj_group:
                    enemies.append({
                        "x": obj.x,
                        "y": obj.y,
                        "type": obj.type if hasattr(obj, 'type') else "night_paladin",
                        "name": obj.name if hasattr(obj, 'name') else "paladin"
                    })
        return enemies

    def _loadNpcs(self):
        npcs = []
        for obj_group in self.tmxData.objectgroups:
            if obj_group.name == "Npcs":
                for obj in obj_group:
                    npcs.append({
                        "x": obj.x,
                        "y": obj.y,
                        "type": obj.type if hasattr(obj, 'type') else "day_AX-400",
                        "name": obj.name if hasattr(obj, 'name') else "AX-400"
                    })
        return npcs

    def _loadSpawnPoints(self):
        spawns = []
        for obj_group in self.tmxData.objectgroups:
            if obj_group.name == "spawnPoint":
                for obj in obj_group:
                   spawns.append((obj.x, obj.y))
        return spawns

    def _loadChangeLvlRects(self):
        rects = []
        for obj_group in self.tmxData.objectgroups:
            if obj_group.name == "changeLvl":
                for obj in obj_group:
                    rects.append({
                        "rect": pygame.Rect(obj.x, obj.y, obj.width, obj.height),
                        "name": getattr(obj, "name", None),
                        "autoTP": obj.properties.get("autoTP", False)
                    })
        return rects

    def _loadCollisionRects(self):
        collisionRects = []
        for obj_group in self.tmxData.objectgroups:
            if obj_group.name == "collides":
                for obj in obj_group:
                    collisionRects.append({
                        "rect": pygame.Rect(obj.x, obj.y, obj.width, obj.height),
                        "is_wallJumpable": obj.properties.get("is_wallJumpable", False)
                    })
        return collisionRects

    def _warnMissingTile(self, layer, x, y):
        if not hasattr(self, '_missing_tile_warnings'):
            self._missing_tile_warnings = set()
        key = (id(layer), x, y)
        if key not in self._missing_tile_warnings:
            self._missing_tile_warnings.add(key)
            print(f"Tuile sans image : carte={self.filepath}, couche={layer.name}, "
                  f"x={x}, y={y}, gid={layer.data[y][x]}")

    def _getLayerSurface(self, layer):
        if not hasattr(self, '_layer_surfs'):
            self._layer_surfs = {}
            
        if layer.name in self._layer_surfs:
            return self._layer_surfs[layer.name]
            
        min_x = min_y = float('inf')
        max_x = max_y = -float('inf')
        has_tiles = False
        for x, y, surf in layer.tiles():
            has_tiles = True
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
            
        if not has_tiles:
            return None
            
        w = (max_x - min_x + 1) * self.tileWidth
        h = (max_y - min_y + 1) * self.tileHeight
        
        layer_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        for x, y, surf in layer.tiles():
            if surf is None:
                self._warnMissingTile(layer, x, y)
                continue
            layer_surf.blit(surf, ((x - min_x) * self.tileWidth, (y - min_y) * self.tileHeight))
            
        self._layer_surfs[layer.name] = layer_surf
        return layer_surf

    def _drawParallaxLayer(self, screen, tmx_data, layer, camera):
        import src.Settings as Settings
        factorX = layer.properties.get("parallax_factor_x", 1.0)
        factorY = layer.properties.get("parallax_factor_y", 1.0)
        
        if layer.properties.get("scale_to_screen", False) or layer.properties.get("is_background", False):
            layer_surf = self._getLayerSurface(layer)
            if not layer_surf: return
            
            zoom = 1.5
            visible_h = int(Settings.SCREEN_HEIGHT / zoom)
            
            scale_factor = visible_h / layer_surf.get_height()
            new_w = int(layer_surf.get_width() * scale_factor)
            new_h = visible_h
            
            if not hasattr(self, '_scaled_surfs'): self._scaled_surfs = {}
            if layer.name not in self._scaled_surfs:
                self._scaled_surfs[layer.name] = pygame.transform.scale(layer_surf, (new_w, new_h))
            img = self._scaled_surfs[layer.name]
            
            offsetX = camera.x * factorX
            offsetY = camera.y * factorY
            draw_x = - (offsetX % new_w)
            
            y_margin = (Settings.SCREEN_HEIGHT - visible_h) / 2
            
            y_shift = layer.properties.get("y_shift", 0)
            
            if layer.properties.get("align_bottom", False):
                draw_y = y_margin + visible_h - new_h - offsetY + y_shift
            else:
                draw_y = y_margin - offsetY + y_shift
                
            while draw_x < Settings.SCREEN_WIDTH:
                screen.blit(img, (draw_x, draw_y))
                draw_x += new_w
            return

        offsetX = camera.x * factorX
        offsetY = camera.y * factorY

        for x, y, surf in layer.tiles():
            gid = layer.data[y][x]
            props = tmx_data.get_tile_properties_by_gid(gid)
            if props and 'frames' in props:
                continue

            if surf is None:
                self._warnMissingTile(layer, x, y)
                continue

            tile_x = (x * self.tileWidth) - offsetX
            tile_y = (y * self.tileHeight) - offsetY
            screen.blit(surf, (tile_x, tile_y))

    def drawMap(self, surface, offset):
        for layer in self.tmxData.visible_layers:
            if hasattr(layer, 'data'):
               self._drawParallaxLayer(surface, self.tmxData, layer, offset)

    def getCollisionRects(self):
        return self.collisionRects

    def _loadCollisionSprites(self):
        collisionSprites = []
        for obj_group in self.tmxData.objectgroups:
            if obj_group.name == "platforms":
                for obj in obj_group:

                    image = self.tmxData.get_tile_image_by_gid(obj.gid)

                    vx = obj.properties.get("vx", 0)
                    vy = obj.properties.get("vy", 0)
                    length = obj.properties.get("length", 0)
                    pause = obj.properties.get("pause", 0)
                    blocking = obj.properties.get("blocking", True)
                    damaging = obj.properties.get("damaging", False)
                    collisionSprites.append(LinearMovingPlatform(obj.x, obj.y, obj.width, obj.height, vx, vy, length, pause, image, blocking, damaging))
            elif obj_group.name == "lasers":
                for obj in obj_group:
                    pause = obj.properties.get("pause", 1200)
                    collisionSprites.append(Laser(obj.x, obj.y, obj.width, obj.height, pause))
            elif obj_group.name == "echelles":
                for obj in obj_group:
                    if hasattr(obj, 'gid') and obj.gid:
                        image = self.tmxData.get_tile_image_by_gid(obj.gid)
                        if image:
                            sprite = pygame.sprite.Sprite()
                            rotation = getattr(obj, 'rotation', 0)
                            if rotation != 0:
                                sprite.image = pygame.transform.rotate(image, -rotation)
                            else:
                                sprite.image = image
                                
                            sprite.rect = sprite.image.get_rect(topleft=(obj.x, obj.y))
                            sprite.is_ladder = True 
                            sprite.blocking = False 
                            collisionSprites.append(sprite)
        return collisionSprites
