import pygame as pg
from src.utils import GameSettings
from src.core import GameManager


class MinimapManager:

    MINIMAP_W = 192
    MINIMAP_H = 108
    MINIMAP_POS = (20, 20)   # 左上角座標 你可改 (x,y)

    def __init__(self, game_manager: GameManager):
        self.game_manager = game_manager

        self.minimap_surface = None     # 完整地圖縮圖
        self.map_key_cached = None      # 紀錄現在哪張地圖  
        self.scale_x = 1
        self.scale_y = 1

    # ---------------------------------------------------------
    # ⚡ 生成縮圖，只會在換地圖時呼叫
    # ---------------------------------------------------------
    def _generate_minimap(self):
        current_key = self.game_manager.current_map_key
        game_map = self.game_manager.maps[current_key]

        # 取得整張 map 的像素大小
        full_w = game_map.tmxdata.width * GameSettings.TILE_SIZE
        full_h = game_map.tmxdata.height * GameSettings.TILE_SIZE

        # 計算縮放比例
        self.scale_x = self.MINIMAP_W / full_w
        self.scale_y = self.MINIMAP_H / full_h

        # 生成縮放地圖
        self.minimap_surface = pg.transform.smoothscale(
            game_map._surface, (self.MINIMAP_W, self.MINIMAP_H)
        )

        # 記錄現在的地圖 key
        self.map_key_cached = current_key

    # ---------------------------------------------------------
    # 🖼️ 繪製小地圖
    # ---------------------------------------------------------
    def draw(self, screen: pg.Surface):

        # 若換地圖 → 重新產生縮圖
        if self.game_manager.current_map_key != self.map_key_cached:
            self._generate_minimap()

        if self.minimap_surface is None:
            return  # 尚未生成縮圖，不畫

        # 先畫縮圖
        screen.blit(self.minimap_surface, self.MINIMAP_POS)

        mx, my = self.MINIMAP_POS

        # -----------------------------------------------------
        # 🟡 玩家位置
        # -----------------------------------------------------
        player = self.game_manager.player
        px = int(player.position.x * self.scale_x) + mx
        py = int(player.position.y * self.scale_y) + my

        pg.draw.circle(screen, (255, 255, 0), (px, py), 4)  # 黃色玩家點

        # -----------------------------------------------------
        # 🔵 NPC / 🔴 敵人 / 🟢 傳送點
        # -----------------------------------------------------
        current_key = self.game_manager.current_map_key

        # NPCs
        for npc in self.game_manager.npcs.get(current_key, []):
            nx = int(npc.position.x * self.scale_x) + mx
            ny = int(npc.position.y * self.scale_y) + my
            pg.draw.circle(screen, (0, 100, 255), (nx, ny), 4)

        # Enemy Trainers
        for enemy in self.game_manager.enemy_trainers.get(current_key, []):
            ex = int(enemy.position.x * self.scale_x) + mx
            ey = int(enemy.position.y * self.scale_y) + my
            pg.draw.circle(screen, (255, 0, 0), (ex, ey), 4)

        # Teleporters
        current_map = self.game_manager.maps[current_key]
        for tp in current_map.teleporters:
            tx = int(tp.pos.x * self.scale_x) + mx
            ty = int(tp.pos.y * self.scale_y) + my
            pg.draw.circle(screen, (0, 255, 0), (tx, ty), 4)

        # -----------------------------------------------------
        # 外框
        # -----------------------------------------------------
        pg.draw.rect(
            screen,
            (255, 255, 255),
            pg.Rect(mx, my, self.MINIMAP_W, self.MINIMAP_H),
            width=2
        )
