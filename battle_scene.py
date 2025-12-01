'''
[TODO HACKATHON 5]
Try to mimic the menu_scene.py or game_scene.py to create this new scene
'''
import pygame as pg
import threading
import time




from src.sprites import BackgroundSprite
from src.scenes.scene import Scene
from src.core import GameManager, OnlineManager
from src.utils import Logger, PositionCamera, GameSettings, Position
from src.core.services import scene_manager, sound_manager, input_manager
from src.sprites import Sprite
from typing import override
from src.interface.components import Button
from src.interface.components.slider import Slider
import random

class BattleScene(Scene):


    def __init__(self):
        super().__init__()
       
        self.background = BackgroundSprite("backgrounds/background1.png")
    
            # 戰鬥狀態
        self.turn = "player"  # "player" 或 "enemy"
        self.battle_state = "choose_action"  # "choose_action", "attacking", "game_over"
        self.message = "What will you do?"
        self.message_timer = 0
        
        # 玩家數據（從 game_manager.bag 獲取第一隻怪獸）
        self.player_monster = {
            "name": "Pikachu",
            "hp": 85,
            "max_hp": 100,
            "attack": 20,
            "sprite_path": "menu_sprites/menusprite1.png"
        }
        
        # 敵人數據
        self.enemy_monster = {
            "name": "Charmander",
            "hp": 80,
            "max_hp": 80,
            "attack": 18,
            "sprite_path": "menu_sprites/menusprite2.png"
        }
        
        # 字體
        self.font_small = pg.font.Font("assets/fonts/Minecraft.ttf", 20)
        self.font_medium = pg.font.Font("assets/fonts/Minecraft.ttf", 30)
        self.font_large = pg.font.Font("assets/fonts/Minecraft.ttf", 40)
        
        # 戰鬥按鈕 - 只在玩家回合顯示
        self.attack_button = Button(
            "UI/raw/UI_Flat_Button02a_3.png", "UI/raw/UI_Flat_Button02a_3.png",
            400, 580, 120, 40,
            self.player_attack
        )
        
        self.run_button = Button(
            "UI/raw/UI_Flat_Button02a_3.png", "UI/raw/UI_Flat_Button02a_3.png",
            640, 580, 120, 40,
            self.run_away
        )
        
        self.item_button = Button(
            "UI/raw/UI_Flat_Button02a_3.png", "UI/raw/UI_Flat_Button02a_3.png",
            880, 580, 120, 40,
            self.use_item
        )
        
        # 載入怪獸圖片
        try:
            self.player_sprite = pg.image.load("assets/images/" + self.player_monster["sprite_path"]).convert_alpha()
            self.player_sprite = pg.transform.scale(self.player_sprite, (150, 150))
        except:
            self.player_sprite = None
            
        try:
            self.enemy_sprite = pg.image.load("assets/images/" + self.enemy_monster["sprite_path"]).convert_alpha()
            self.enemy_sprite = pg.transform.scale(self.enemy_sprite, (150, 150))
        except:
            self.enemy_sprite = None

    def player_attack(self):
        """玩家攻擊"""
        if self.turn != "player" or self.battle_state != "choose_action":
            return
            
        # 計算傷害（加入隨機性）
        damage = self.player_monster["attack"] + random.randint(-5, 5)
        self.enemy_monster["hp"] -= damage
        
        # 確保 HP 不會小於 0
        if self.enemy_monster["hp"] < 0:
            self.enemy_monster["hp"] = 0
        
        self.message = f"{self.player_monster['name']} attacks! Deals {damage} damage!"
        self.message_timer = 2.0
        self.battle_state = "attacking"
        
        # 檢查敵人是否死亡
        if self.enemy_monster["hp"] <= 0:
            self.message = f"{self.enemy_monster['name']} fainted! You win!"
            self.battle_state = "game_over"
        else:
            # 切換到敵人回合
            self.turn = "enemy"

    def enemy_attack(self):
        """敵人攻擊"""
        if self.enemy_monster["hp"] <= 0:
            return
            
        # 計算傷害
        damage = self.enemy_monster["attack"] + random.randint(-5, 5)
        self.player_monster["hp"] -= damage
        
        if self.player_monster["hp"] < 0:
            self.player_monster["hp"] = 0
        
        self.message = f"{self.enemy_monster['name']} attacks! Deals {damage} damage!"
        self.message_timer = 2.0
        
        # 檢查玩家是否死亡
        if self.player_monster["hp"] <= 0:
            self.message = f"{self.player_monster['name']} fainted! You lose!"
            self.battle_state = "game_over"
        else:
            # 切換回玩家回合
            self.turn = "player"
            self.battle_state = "choose_action"
            self.message = "What will you do?"

    def run_away(self):
        """逃跑"""
        if self.turn != "player" or self.battle_state != "choose_action":
            return
            
        # 50% 機率逃跑成功
        if random.random() < 0.5:
            self.message = "Got away safely!"
            self.message_timer = 1.5
            self.battle_state = "game_over"
        else:
            self.message = "Can't escape!"
            self.message_timer = 2.0
            self.turn = "enemy"
            self.battle_state = "attacking"

    def use_item(self):
        """使用道具（回復 HP）"""
        if self.turn != "player" or self.battle_state != "choose_action":
            return
            
        # 簡單的回復道具
        heal = 30 #之後用item
        self.player_monster["hp"] += heal
        
        if self.player_monster["hp"] > self.player_monster["max_hp"]:
            self.player_monster["hp"] = self.player_monster["max_hp"]
        
        self.message = f"{self.player_monster['name']} restored {heal} HP!"
        self.message_timer = 2.0
        self.battle_state = "attacking"
        self.turn = "enemy"

    @override
    def enter(self) -> None:
        sound_manager.play_bgm("RBY 107 Battle! (Trainer).ogg")
        sound_manager.set_bgm_volume(GameSettings.AUDIO_VOLUME)
        
        # 重置戰鬥狀態
        self.turn = "player"
        self.battle_state = "choose_action"
        self.message = "A wild enemy appeared!"
        self.message_timer = 2.0

    @override
    def exit(self) -> None:
        pass

    @override
    def update(self, dt: float):
        # 更新訊息計時器
        if self.message_timer > 0:
            self.message_timer -= dt
            
            # 當訊息顯示完畢且在攻擊狀態，執行敵人攻擊
            if self.message_timer <= 0 and self.battle_state == "attacking":
                if self.turn == "enemy":
                    self.enemy_attack()
                elif self.turn == "player":
                    self.battle_state = "choose_action"
        
        # 遊戲結束後自動返回
        if self.battle_state == "game_over" and self.message_timer <= 0:
            scene_manager.change_scene("game")
        
        # 只在玩家回合且選擇動作時更新按鈕
        if self.turn == "player" and self.battle_state == "choose_action":
            self.attack_button.update(dt)
            self.run_button.update(dt)
            self.item_button.update(dt)

    @override
    def draw(self, screen: pg.Surface) -> None:
        self.background.draw(screen)
        
        '''# 繪製戰鬥區域背景
        battle_bg = pg.Surface((1000, 450))
        battle_bg.set_alpha(200)
        battle_bg.fill((50, 50, 50))
        screen.blit(battle_bg, (200, 100))'''
        
        # 繪製敵人怪獸（右上）
        if self.enemy_sprite:
            screen.blit(self.enemy_sprite, (900, 100))
        
        # 繪製敵人資訊
        enemy_name = self.font_medium.render(self.enemy_monster["name"], True, (255, 255, 255))
        screen.blit(enemy_name, (850, 50))
        
        # 敵人 HP 條
        hp_ratio = self.enemy_monster["hp"] / self.enemy_monster["max_hp"]
        self.draw_hp_bar(screen, 650, 280, 200, 20, hp_ratio)
        enemy_hp_text = self.font_small.render(
            f"HP: {self.enemy_monster['hp']}/{self.enemy_monster['max_hp']}", 
            True, (255, 255, 255)
        )
        screen.blit(enemy_hp_text, (650, 305))
        
        # 繪製玩家怪獸（左下）
        if self.player_sprite:
            screen.blit(self.player_sprite, (150, 250))
        
        # 繪製玩家資訊
        player_name = self.font_small.render(self.player_monster["name"], True, (255, 255, 255))
        screen.blit(player_name, (100, 400))
        
        # 玩家 HP 條
        hp_ratio = self.player_monster["hp"] / self.player_monster["max_hp"]
        self.draw_hp_bar(screen, 100, 450, 200, 20, hp_ratio)
        player_hp_text = self.font_small.render(
            f"HP: {self.player_monster['hp']}/{self.player_monster['max_hp']}", 
            True, (255, 255, 255)
        )
        screen.blit(player_hp_text, (100, 475))
        
        # 繪製訊息框
        message_bg = pg.Surface((1280, 200))
        message_bg.set_alpha(220)
        message_bg.fill((30, 30, 30))
        screen.blit(message_bg, (0, 500))
        
        # 繪製訊息文字
        message_text = self.font_medium.render(self.message, True, (255, 255, 255))
        screen.blit(message_text, (200, 520))
        
        # 繪製回合指示器
        turn_text = self.font_small.render(
            f"Turn: {self.turn.upper()}", 
            True, (255, 255, 0)
        )
        screen.blit(turn_text, (450, 20))
        
        # 只在玩家回合且可以選擇動作時顯示按鈕
        if self.turn == "player" and self.battle_state == "choose_action" and self.message_timer <= 0:
            # 繪製按鈕背景和文字
            self.attack_button.draw(screen)
            attack_text = self.font_small.render("ATTACK", True, (0, 0, 0))
            screen.blit(attack_text, (410, 590))
            
            self.run_button.draw(screen)
            run_text = self.font_small.render("RUN", True, (0, 0, 0))
            screen.blit(run_text, (650, 590))
            
            self.item_button.draw(screen)
            item_text = self.font_small.render("ITEM", True, (0, 0, 0))
            screen.blit(item_text, (890, 590))

    def draw_hp_bar(self, screen, x, y, width, height, ratio):
        """繪製 HP 血條"""
        # 背景（紅色）
        pg.draw.rect(screen, (200, 0, 0), (x, y, width, height))
        
        # HP（綠色到黃色到紅色）
        if ratio > 0.5:
            color = (0, 255, 0)  # 綠色
        elif ratio > 0.2:
            color = (255, 255, 0)  # 黃色
        else:
            color = (255, 0, 0)  # 紅色
            
        pg.draw.rect(screen, color, (x, y, width * ratio, height))
        
        # 邊框
        pg.draw.rect(screen, (255, 255, 255), (x, y, width, height), 2)