# src/scenes/gym_scene.py
import pygame as pg
from src.scenes.scene import Scene
from src.core import GameManager
from src.core.services import scene_manager, input_manager
from src.utils import PositionCamera, GameSettings # 根據需要引入

class GymScene(Scene):
    """專門處理 Gym 內部的邏輯和 UI (例如：戰鬥、NPC 對話)。"""
    game_manager: GameManager
    
    def __init__(self, game_manager: GameManager):
        super().__init__()
        self.game_manager = game_manager
        # GymScene 專屬狀態
        self.is_battle_prep = True # 是否在準備狀態 (例如：問是否開始戰鬥)

    def update(self, dt: float):
        # 核心：在 update 裡處理退出邏輯
        if self.is_battle_prep:
            # 繪製準備 UI (例如詢問是否開始戰鬥)
            # 檢查按鍵 (避免 handle_event)
            if input_manager.key_just_pressed(pg.K_y):
                self.is_battle_prep = False # 開始戰鬥邏輯
                # 這裡可以切換到 BattleScene: scene_manager.change_scene("battle")
                
            elif input_manager.key_just_pressed(pg.K_n) or input_manager.key_just_pressed(pg.K_ESCAPE):
                self.exit_gym() # 離開
        
        # 執行 Gym 內部的戰鬥/謎題/其他邏輯
        # ...
    
    def draw(self, screen: pg.Surface):
        # 確保 Gym 的背景被繪製 (可以繪製 Gym 地圖或一個專屬背景)
        self.game_manager.current_map.draw(screen, PositionCamera(0, 0)) # 假設 Gym map 已經載入
        
        # 繪製 Gym 專屬的 UI/對話框
        if self.is_battle_prep:
            # 繪製詢問框：是否開始戰鬥？ (Y/N)
            pass
            
    def exit_gym(self):
        """返回到 GameScene。"""
        # 確保玩家回到 GameScene 時的位置是 Gym 的出口
        # 這裡會觸發 try_switch_map 邏輯
        self.game_manager.switch_map(self.game_manager.last_map_key) # 假設您在 GameManager 中儲存了上一個地圖 key
        scene_manager.change_scene("game")

    # (您可以刪除 handle_event 確保不被使用)
    # def handle_event(self, event):
    #     pass