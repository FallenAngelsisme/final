from __future__ import annotations
import pygame as pg
from .entity import Entity
from src.core.services import input_manager
from src.utils import Position, PositionCamera, GameSettings, Logger, Direction
from src.core import GameManager
import math
from typing import override

class Player(Entity):
    speed: float = 4.0 * GameSettings.TILE_SIZE
    game_manager: GameManager

    def __init__(self, x: float, y: float, game_manager: GameManager) -> None:
        super().__init__(x, y, game_manager)

    @override
    def update(self, dt: float) -> None:
        dis = Position(0, 0)
        '''
        [TODO HACKATHON 2]
        Calculate the distance change, and then normalize the distance
        
        [TODO HACKATHON 4]
        Check if there is collision, if so try to make the movement smooth
        Hint #1 : use entity.py _snap_to_grid function or create a similar function
        Hint #2 : Beware of glitchy teleportation, you must do
                    1. Update X
                    2. If collide, snap to grid
                    3. Update Y
                    4. If collide, snap to grid
                  instead of update both x, y, then snap to grid
        
        if input_manager.key_down(pg.K_LEFT) or input_manager.key_down(pg.K_a):
            dis.x -= ...
        if input_manager.key_down(pg.K_RIGHT) or input_manager.key_down(pg.K_d):
            dis.x += ...
        if input_manager.key_down(pg.K_UP) or input_manager.key_down(pg.K_w):
            dis.y -= ...
        if input_manager.key_down(pg.K_DOWN) or input_manager.key_down(pg.K_s):
            dis.y += ...
        
        self.position = ...
        '''
        
        if input_manager.key_down(pg.K_LEFT) or input_manager.key_down(pg.K_a):
            dis.x -= 1
            self.direction = Direction.LEFT
            self.animation.switch("left")
        if input_manager.key_down(pg.K_RIGHT) or input_manager.key_down(pg.K_d):
            dis.x += 1
            self.direction = Direction.RIGHT
            self.animation.switch("right")  
        if input_manager.key_down(pg.K_UP) or input_manager.key_down(pg.K_w):
            dis.y -= 1
            self.direction = Direction.UP
            self.animation.switch("up")
        if input_manager.key_down(pg.K_DOWN) or input_manager.key_down(pg.K_s):
            dis.y += 1
            self.direction = Direction.DOWN
            self.animation.switch("down")
        
        
        #print(f"dis before normalize: {dis.x}, {dis.y}")
        #正規化向量
        magnitude = math.hypot(dis.x, dis.y)
        #print(f"new position: {self.position.x}, {self.position.y}")
        if magnitude > 0:
            dis.x = dis.x / magnitude * self.speed * dt
            dis.y = dis.y / magnitude * self.speed * dt
        
         # move with collision handling
        # X方向移動
        self.position.x += dis.x
        player_rect = pg.Rect(self.position.x, self.position.y, GameSettings.TILE_SIZE, GameSettings.TILE_SIZE)
        collide = self.game_manager.current_map.check_collision(player_rect)
        for enemy in self.game_manager.current_enemy_trainers:
            enemy_rect = pg.Rect(enemy.position.x, enemy.position.y, GameSettings.TILE_SIZE, GameSettings.TILE_SIZE)
            #一樣也是!!#物品1.colliderect(物2)
            if player_rect.colliderect(enemy_rect):
                collide = True
                break
        if collide:
            self.position.x = self._snap_to_grid(self.position.x)

        # Y方向移動
        self.position.y += dis.y
        player_rect = pg.Rect(self.position.x, self.position.y, GameSettings.TILE_SIZE, GameSettings.TILE_SIZE)
        collide = self.game_manager.current_map.check_collision(player_rect)#用圖去判斷
        for enemy in self.game_manager.current_enemy_trainers:
            enemy_rect = pg.Rect(enemy.position.x, enemy.position.y, GameSettings.TILE_SIZE, GameSettings.TILE_SIZE)
            #一樣也是!!#物品1.colliderect(物2)
            if player_rect.colliderect(enemy_rect):
                collide = True
                break
        if collide:
            self.position.y = self._snap_to_grid(self.position.y)


        # Check teleportation 角色移動的更新迴圈，實際觸發傳送邏輯。它會呼叫 current_map.check_telepor
        tp = self.game_manager.current_map.check_teleport(self.position)
        if tp:
            #dest = tp.destination
            #self.game_manager.switch_map(dest)
                              #切地圖的入口開關
                                        # json裡面喔 tp["destination"]
            self.game_manager.switch_map(tp.destination)

        super().update(dt)

    @override
    def draw(self, screen: pg.Surface, camera: PositionCamera) -> None:
        super().draw(screen, camera)
        
    @override
    def to_dict(self) -> dict[str, object]:
        return super().to_dict()
    
    @classmethod
    @override
    def from_dict(cls, data: dict[str, object], game_manager: GameManager) -> Player:
        return cls(data["x"] * GameSettings.TILE_SIZE, data["y"] * GameSettings.TILE_SIZE, game_manager)

