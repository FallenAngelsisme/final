import pygame as pg
import threading
import time
import json
import pygame



from src.scenes.scene import Scene
from src.core import GameManager, OnlineManager
from src.utils import Logger, PositionCamera, GameSettings, Position
from src.core.services import sound_manager,input_manager,scene_manager
from src.sprites import Sprite
from typing import override
from src.interface.components import Button#my2
from src.interface.components.slider import Slider#my2
from src.core.managers.minimap_manager import MinimapManager







class GameScene(Scene):
    game_manager: GameManager
    online_manager: OnlineManager | None
    sprite_online: Sprite
   
    def __init__(self):
        super().__init__()
        #minimap
        self.game_manager = None
        self.minimap = None
        #
        self.warning_sign = Sprite(
            "exclamation.png",
            (GameSettings.TILE_SIZE // 2, GameSettings.TILE_SIZE // 2)
        )
        


        # Overlay 狀態
        self.is_overlay_open = False
        self.is_bag_overlay_open = False

        # ★ NEW: 金錢 UI 
        self.coin_icon = pg.image.load("assets/images/ingame_ui/coin.png").convert_alpha()
        self.coin_icon = pg.transform.scale(self.coin_icon, (30, 30))

        #buttom
        px, py = GameSettings.SCREEN_WIDTH // 2, GameSettings.SCREEN_HEIGHT // 2
        self.bag = Button(
            "UI/button_backpack.png", "UI/button_backpack_hover.png",
            GameSettings.SCREEN_WIDTH-170, 20, 60, 60,# x, y 座標
            self.open_bag
            #lambda: scene_manager.change_scene("game")
        )#my2
        self.setting_button = Button(
            "UI/button_setting.png", "UI/button_setting_hover.png",
            GameSettings.SCREEN_WIDTH-100, 20, 60, 60,# x, y 座標
            self.open_overlay
            #lambda: scene_manager.change_scene("game")
        )#my2
        self.btn_back = Button(
            "UI/button_back.png", "UI/button_back_hover.png",
            300, 440,
            60, 60,
            self.close_overlay
        )
        
        self.save_button = Button(
            "UI/button_save.png","UI/button_save_hover.png",
            x=300, y=360, width=60, height=60,
            on_click=self.save_game
        )

        self.load_button = Button(
            "UI/button_load.png","UI/button_load_hover.png",
            x=370, y=360, width=60, height=60,
            on_click=self.load_game
        )

        #
        

        

        self.back_image = pg.image.load("assets/images/UI/raw/UI_Flat_Frame03a.png").convert_alpha()
        self.back_image = pg.transform.scale(self.back_image, (800, 520))  # 寬高
       
        self.vol_max_width = 700
        self.vol_height = 20
       
        #knob_image = pg.image.load("assets/images/UI/raw/UI_Flat_Handle03a.png").convert_alpha()
        self.volume_slider = Slider(
            x=300,
            y=260,   # 這裡是滑桿 Y 座標
            width=self.vol_max_width,
            height=self.vol_height,
            min_value=0,
            max_value=1,
            initial_value=GameSettings.AUDIO_VOLUME,
            knob_img="UI/raw/UI_Flat_Handle03a.png",
            knob_width=30,    
            knob_height=30
        )

        # MUTE BUTTON
        self.is_muted = False
        #####
        self.saved_volume = GameSettings.AUDIO_VOLUME

        self.mute_button = Button(
            img_path="UI/raw/UI_Flat_ToggleOff03a.png",
            img_hovered_path="UI/raw/UI_Flat_ToggleOff03a.png",      # toggle 不用 hover
            x=400, y=300, width=40, height=40,
            on_click=self.toggle_mute,
            img_on="UI/raw/UI_Flat_ToggleOn03a.png",
            img_off="UI/raw/UI_Flat_ToggleOff03a.png"
        )
        #字
                                 #None表預設字型 or  我這裡有設                                     #60是字大小
        self.font_small  = pg.font.Font("assets/fonts/Minecraft.ttf", 20)
        self.font_medium = pg.font.Font("assets/fonts/Minecraft.ttf", 30)
        self.font_large  = pg.font.Font("assets/fonts/Minecraft.ttf", 60)
        self.texts = [
        ("Setting ", self.font_large, (600, 150)),
        ("Volume",  self.font_medium,(300, 220)),
        ("Mute",self.font_medium, (300, 300))
        ]

        # 儲存/讀取訊息顯示
        self.message_text = ""
        self.message_timer = 0
        self.message_duration = 2.0  # 訊息顯示2秒

        # Game Manager
        manager = GameManager.load("saves/game0.json")
        if manager is None:
            Logger.error("Failed to load game manager")
            exit(1)
        self.game_manager = manager
       
        # Online Manager
        if GameSettings.IS_ONLINE:
            self.online_manager = OnlineManager()
        else:
            self.online_manager = None
        self.sprite_online = Sprite("ingame_ui/options1.png", (GameSettings.TILE_SIZE, GameSettings.TILE_SIZE))
       
        #button 生效時!我需要
    def open_overlay(self):
        self.is_overlay_open = True
        self.volume_slider.value = GameSettings.AUDIO_VOLUME  # ← 新增
        self.volume_slider.update_knob_position()  


    def close_overlay(self):
        self.is_overlay_open = False

    def open_bag(self):
        self.game_manager.bag.toggle()



    def toggle_mute(self):
        self.is_muted = not self.is_muted
        if self.is_muted:
            sound_manager.set_bgm_volume(0)
        else:
            sound_manager.set_bgm_volume(self.volume_slider.value)


    def save_game(self):
        """儲存遊戲狀態"""
        try:
            if self.game_manager and self.game_manager.player:
                # 更新當前地圖的玩家位置
                current_map = self.game_manager.current_map
                current_map.spawn = Position(
                    self.game_manager.player.position.x,
                    self.game_manager.player.position.y
                )
                
                # 儲存到檔案
                self.game_manager.save("saves/game0.json")
                self.show_message("Game Saved!")
                Logger.info(f"Game saved at position: ({self.game_manager.player.position.x}, {self.game_manager.player.position.y})")
            else:
                self.show_message("Save Failed!")
                Logger.warning("Cannot save: player is None")
        except Exception as e:
            self.show_message("Save Failed!")
            Logger.error(f"Failed to save game: {e}")

    def load_game(self):
        """讀取遊戲狀態"""
        try:
            # 重新載入遊戲資料
            manager = GameManager.load("saves/game0.json")
            if manager is None:
                self.show_message("Load Failed!")
                Logger.error("Failed to load game manager")
                return
            
            # 保存舊的 online_manager
            old_online = self.online_manager
            
            # 更新 game_manager
            self.game_manager = manager
            self.online_manager = old_online
            
            # 確保玩家位置正確設置
            if self.game_manager.player:
                # 從存檔讀取的位置已經是像素座標
                spawn_pos = self.game_manager.current_map.spawn
                self.game_manager.player.position = Position(spawn_pos.x, spawn_pos.y)
                
                # 強制更新相機位置，避免畫面跳動
                self.game_manager.player.animation.update_pos(self.game_manager.player.position)
                
                self.show_message("Game Loaded!")
                Logger.info(f"Game loaded at position: ({spawn_pos.x}, {spawn_pos.y})")
            else:
                self.show_message("Load Failed!")
                Logger.warning("Loaded game has no player")
                
        except Exception as e:
            self.show_message("Load Failed!")
            Logger.error(f"Failed to load game: {e}")

    def show_message(self, text: str):
        """顯示訊息"""
        self.message_text = text
        self.message_timer = self.message_duration

    @override
    def enter(self) -> None:
        sound_manager.play_bgm("RBY 103 Pallet Town.ogg")
        #sound_manager.set_bgm_volume(self.volume_slider.value)
        if not self.is_muted:
            sound_manager.set_bgm_volume(GameSettings.AUDIO_VOLUME)
        else:
            sound_manager.set_bgm_volume(0)
        if self.online_manager:
            self.online_manager.enter()
        
        #minimap
        
        self.minimap = MinimapManager(self.game_manager)
    @override
    def exit(self) -> None:
        if self.online_manager:
            self.online_manager.exit()
       
    @override
    def update(self, dt: float):
        # Check if there is assigned next scene
        self.game_manager.try_switch_map()
       
        # Update player and other data
        if self.game_manager.player:
            self.game_manager.player.update(dt)
        for enemy in self.game_manager.current_enemy_trainers:
            enemy.update(dt)
            if enemy.detected and input_manager.key_pressed(pygame.K_SPACE):
                
                scene_manager.change_scene("battle") 

        for npc in self.game_manager.current_npcs:
            npc.update(dt)
            if npc.detected and input_manager.key_pressed(pygame.K_SPACE):
    
                from src.scenes.shop_scene import ShopScene
                scene_manager.register_scene("shop", ShopScene(self.game_manager))
                scene_manager.change_scene("shop")

        if self.game_manager.player:
            player_rect = pg.Rect(
                self.game_manager.player.position.x,
                self.game_manager.player.position.y,
                GameSettings.TILE_SIZE,
                GameSettings.TILE_SIZE
            )
            for bush_rect in self.game_manager.current_map._bush_map:
                if player_rect.colliderect(bush_rect) and pg.key.get_pressed()[pg.K_SPACE]:
                    # 進入抓寶可夢場景
                    from src.scenes.catch_scene import CatchPokemonScene
                    scene_manager.register_scene("catch", CatchPokemonScene(self.game_manager))
                    scene_manager.change_scene("catch")
                    break  # 避免一次碰撞多次觸發
                
        # Update others
        self.game_manager.bag.update(dt)
       
        if self.game_manager.player is not None and self.online_manager is not None:
            _ = self.online_manager.update(
                self.game_manager.player.position.x,
                self.game_manager.player.position.y,
                self.game_manager.current_map.path_name
            )
        self.setting_button.update(dt)#my2
        self.bag.update(dt)#my2
       
        if self.game_manager.bag.visible:
            self.game_manager.bag.update(dt)
            return
        
        if self.is_overlay_open:
            self.btn_back.update(dt)
            self.load_button.update(dt)
            self.save_button.update(dt)
            #vol
            self.mute_button.update(dt)
            old_value = self.volume_slider.value
            self.volume_slider.update(dt)
            if not self.is_muted:
                if abs(self.volume_slider.value - old_value) > 0.001:
                    GameSettings.AUDIO_VOLUME = self.volume_slider.value
                    self.saved_volume = self.volume_slider.value
                    sound_manager.set_bgm_volume(self.volume_slider.value)
            
            else:
                # 靜音時，滑桿移動會更新 saved_volume，但不影響實際播放音量
                if abs(self.volume_slider.value - old_value) > 0.001:
                    self.saved_volume = self.volume_slider.value
                    GameSettings.AUDIO_VOLUME = self.volume_slider.value

        
        

        

         # 更新訊息計時器
        if self.message_timer > 0:
            self.message_timer -= dt
            

    @override
    def draw(self, screen: pg.Surface):  
        player = self.game_manager.player      
        if self.game_manager.player:
            '''
            [TODO HACKATHON 3]
            Implement the camera algorithm logic here
            Right now it's hard coded, you need to follow the player's positions
            you may use the below example, but the function still incorrect, you may trace the entity.py
           
            camera = self.game_manager.player.camera
            '''
            ####
            if GameSettings.DEBUG:  # 如果有 debug 模式
                Logger.info(f"Player position: {self.game_manager.player.position.x}, {self.game_manager.player.position.y}")
            #camera = PositionCamera(16 * GameSettings.TILE_SIZE, 30 * GameSettings.TILE_SIZE) 固定鏡頭
            camera = self.game_manager.player.camera #在entity.py裡面有 camera(self) 裡面用player的position算鏡頭位置
            #所以這裡用play.camera
            self.game_manager.current_map.draw(screen, camera)
            self.game_manager.player.draw(screen, camera)
        else:
            Logger.warning("Player is None!")
            camera = PositionCamera(0, 0)
            self.game_manager.current_map.draw(screen, camera)
       
        for enemy in self.game_manager.current_enemy_trainers:
            enemy.draw(screen, camera)

        for npc in self.game_manager.current_npcs:
            npc.draw(screen, camera)
        
       

        self.minimap.draw(screen)

        self.game_manager.bag.draw(screen)
       
        if self.online_manager and self.game_manager.player:
            list_online = self.online_manager.get_list_players()
            for player in list_online:
                if player["map"] == self.game_manager.current_map.path_name:
                    cam = self.game_manager.player.camera
                    pos = cam.transform_position_as_position(Position(player["x"], player["y"]))
                    self.sprite_online.update_pos(pos)
                    self.sprite_online.draw(screen)
       
       
       


        self.bag.draw(screen) #my2
        self.setting_button.draw(screen)
        # ★ NEW: 繪製金錢 (Requirement 2)
        if self.game_manager and self.game_manager.bag:
            money = self.game_manager.bag._money
            
            coin_x = GameSettings.SCREEN_WIDTH - 280 
            coin_y = 20
            
            screen.blit(self.coin_icon, (coin_x, coin_y))

            money_text = self.font_medium.render(f"{money}", True, (255, 255, 255)) 
            screen.blit(money_text, (coin_x + 35, coin_y + 4))
        # Overlay
        if self.is_overlay_open:
            # 暗背景
                #建立一個新的層
            overlay = pg.Surface((GameSettings.SCREEN_WIDTH, GameSettings.SCREEN_HEIGHT))
                #alpha是指 整體透明度
            overlay.set_alpha(180)
                #填上顏色
            overlay.fill((0, 0, 0))
                #貼到主畫上
            screen.blit(overlay, (0, 0))

            # Overlay 內容
            screen.blit(self.back_image, (250, 100)) #位置

            self.volume_slider.draw(screen)
            self.mute_button.draw(screen)
            self.load_button.draw(screen)
            self.save_button.draw(screen)
        
            for text, font, pos in self.texts:
                text_surface = font.render(text, True, (0,0,0))
                screen.blit(text_surface, pos)
           
            volume_percent = int(self.volume_slider.value * 100)
            volume_value = self.font_medium.render(f"{volume_percent}%", True, (255, 255, 255))
            screen.blit(volume_value, (500, 220))
            # 返回
            self.btn_back.draw(screen)

            #self.game_manager.bag.draw(screen)
        
     
        

        # 顯示儲存/讀取訊息
        if self.message_timer > 0:
            message_surface = self.font_medium.render(self.message_text, True, (255, 255, 255))
            message_rect = message_surface.get_rect(center=(GameSettings.SCREEN_WIDTH // 2, 50))
            
            # 半透明背景
            bg_rect = pg.Rect(message_rect.x - 10, message_rect.y - 5, 
                            message_rect.width + 20, message_rect.height + 10)
            bg_surface = pg.Surface((bg_rect.width, bg_rect.height))
            bg_surface.set_alpha(200)
            bg_surface.fill((0, 0, 0))
            screen.blit(bg_surface, bg_rect)
            
            # 訊息文字
            screen.blit(message_surface, message_rect)

    """def handle_event(self, event):
        print("[GameScene] Event:", event)
        if self.is_overlay_open:
            self.btn_back.handle_event(event)
            self.load_button.handle_event(event)
            self.save_button.handle_event(event)
            self.mute_button.handle_event(event)
            self.volume_slider.handle_event(event)
            return  # 覆蓋層打開時攔截所有事件
    
        # ========== 2. 處理背包內部事件（包括進化按鈕）==========
        # ⭐ 關鍵：先處理背包內容，再處理背包按鈕
        if self.game_manager.bag.visible:
            # Bag 有處理事件 → 就 return
            if self.game_manager.bag.handle_event(event):
                return

            # Bag 開著 → 阻擋遊戲操作（但保留按鈕事件）
            return
        
        
        self.bag.handle_event(event)
        self.setting_button.handle_event(event)
        
        # ========== 4. 其他遊戲事件 ==========
        # 玩家移動、互動等..."""