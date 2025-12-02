import pygame as pg
import json
from src.utils import GameSettings
from src.utils.definition import Monster, Item
from src.utils import Logger
from src.interface.components import Button
import os
class Bag:
    _monsters_data: list[Monster]
    _items_data: list[Item]
    PAGE_SIZE = 4 #UI
    def __init__(self, monsters_data: list[Monster] | None = None, items_data: list[Item] | None = None):
        self._monsters_data = monsters_data if monsters_data else []
        self._items_data = items_data if items_data else []


        src = "assets/images/UI/raw/UI_Flat_ButtonPlay01a.png"
        dst = "assets/images/UI/raw/UI_Flat_ButtonPlay01a_left.png"

        if not os.path.exists(dst):
            img = pg.image.load(src).convert_alpha()
            flipped = pg.transform.flip(img, True, False)
            pg.image.save(flipped, dst)
            Logger.info(f"Generated flipped button: {dst}")

        # UI
        self.bg_img = pg.image.load("assets/images/UI/raw/UI_Flat_Frame03a.png").convert_alpha()
        self.bg_img = pg.transform.scale(self.bg_img, (800, 520))

        self.visible = False
        self.current_page = 0
        self.current_tab = "monster"

        self.monster_card_bg = pg.image.load("assets/images/UI/raw/UI_Flat_Banner03a.png").convert_alpha()
        self.monster_card_bg = pg.transform.scale(self.monster_card_bg, (310, 75))

        self.item_card_bg = pg.image.load("assets/images/UI/raw/UI_Flat_Banner03a.png").convert_alpha()
        self.item_card_bg = pg.transform.scale(self.item_card_bg, (310, 75))

        self.font_small  = pg.font.Font("assets/fonts/Minecraft.ttf", 15)
        self.font_medium = pg.font.Font("assets/fonts/Minecraft.ttf", 24)
        self.font_large  = pg.font.Font("assets/fonts/Minecraft.ttf", 30)

         # Tab 按鈕
        #640
        self.btn_tab_mon = Button(
            img_path="UI/raw/UI_Flat_Banner02a.png", img_hovered_path="UI/raw/UI_Flat_Banner02a.png",
            x=460, y=140, width=140, height=35,
            on_click=lambda: self.switch_tab("monster")
        )
        self.btn_tab_item = Button(
            img_path="UI/raw/UI_Flat_Banner02a.png", img_hovered_path="UI/raw/UI_Flat_Banner02a.png",
            x=700, y=140, width=140, height=35,
            on_click=lambda: self.switch_tab("item")
        )

        # 分頁按鈕
        #640
        self.btn_prev = Button(
            img_path="UI/raw/UI_Flat_ButtonPlay01a_left.png", img_hovered_path="UI/raw/UI_Flat_ButtonPlay01a_left.png",
            x=500, y=560, width=50, height=30,
            on_click=self.prev_page
        )
        self.btn_next = Button(
            img_path="UI/raw/UI_Flat_ButtonPlay01a.png", img_hovered_path="UI/raw/UI_Flat_ButtonPlay01a.png",
            x=780, y=560, width=50, height=30,
            on_click=self.next_page
        )

        # 關閉按鈕（右上角）
        self.btn_close = Button(
            img_path="UI/button_x.png", img_hovered_path="UI/button_x_hover.png",
            x=950, y=140, width=40, height=40,
            on_click=self.toggle
        )




    def handle_event(self, event):
        if not self.visible:
            return

        self.btn_prev.handle_event(event)
        self.btn_next.handle_event(event)
        self.btn_close.handle_event(event)

        self.btn_tab_mon.handle_event(event)
        self.btn_tab_item.handle_event(event)

    
    def prev_page(self):
        self.current_page = max(self.current_page - 1, 0)

    def next_page(self):
        max_p = self.get_max_pages()
        self.current_page = min(self.current_page + 1, max_p)

    def get_max_pages(self):
        total = len(self._monsters_data) if self.current_tab == "monster" else len(self._items_data)
        return max((total - 1) // Bag.PAGE_SIZE, 0)
    
    
    def switch_tab(self, tab):
        self.current_tab = tab
        self.current_page = 0

    def toggle(self):
        self.visible = not self.visible

    def update(self, dt: float):
        if not self.visible:
            return
        
        self.btn_prev.update(dt)
        self.btn_next.update(dt)
        self.btn_close.update(dt)
        self.btn_tab_mon.update(dt)
        self.btn_tab_item.update(dt)

    def draw(self, screen: pg.Surface):
        if not self.visible:
            return
        overlay = pg.Surface((GameSettings.SCREEN_WIDTH, GameSettings.SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        screen.blit(self.bg_img, (250, 100))

        # Tabs
        self.draw_tabs(screen)

        # 分頁
        self.btn_prev.draw(screen)
        self.btn_next.draw(screen)

        # 關閉按鈕
        self.btn_close.draw(screen)

        if self.current_tab == "monster":
            self.draw_monsters(screen)
        else:
            self.draw_items(screen)

        
    def draw_tabs(self, screen):
        self.btn_tab_mon.draw(screen)
        self.btn_tab_item.draw(screen)

        txt1 = self.font_small.render("Monsters", True, (0, 0, 0))
        txt2 = self.font_small.render("Items", True, (0, 0, 0))

        screen.blit(txt1, (490, 148))
        screen.blit(txt2, (730, 148))

         #   繪製 Monster 列表
    def draw_monsters(self, screen):
        start = self.current_page * Bag.PAGE_SIZE
        mons = self._monsters_data[start:start + Bag.PAGE_SIZE]

        x = 505
        y = 180

        for mon in mons:
            screen.blit(self.monster_card_bg, (x, y))

            img = pg.image.load("assets/images/" + mon.sprite_path).convert_alpha()
            img = pg.transform.scale(img, (65, 65))
            screen.blit(img, (x + 10, y + 5))

            # 名字
            screen.blit(self.font_medium.render(mon.name, True, (0, 0, 0)), (x + 80, y + 10))
            screen.blit(self.font_small.render(f"Lv.{mon.level}", True, (0, 0, 0)), (x + 250, y + 10))

            # HP bar
            pg.draw.rect(screen, (40, 40, 40), (x + 80, y + 35, 200, 12))
            hp_ratio = mon.hp / mon.max_hp
            pg.draw.rect(screen, (0, 200, 0), (x + 80, y + 35, int(200 * hp_ratio), 12))

            hp_text = self.font_small.render(f"{mon.hp}/{mon.max_hp}", True, (0, 0, 0))
            screen.blit(hp_text, (x + 140, y + 50))

            y += 100

   
    #Item UI
    def draw_items(self, screen):
        start = self.current_page * Bag.PAGE_SIZE
        items = self._items_data[start:start + Bag.PAGE_SIZE]

        x = 505
        y = 180

        for item in items:
            screen.blit(self.item_card_bg, (x, y))

            img = pg.image.load("assets/images/" + item.sprite_path).convert_alpha()
            img = pg.transform.scale(img, (45, 45))
            screen.blit(img, (x + 10, y + 15))

            screen.blit(self.font_medium.render(item.name, True, (0, 0, 0)), (x + 70, y + 10))
            screen.blit(self.font_small.render(f"x{item.count}", True, (0, 0, 0)), (x + 250, y + 40))

            y += 90
    
    def to_dict(self) -> dict[str, object]:
        '''
        return {
            "monsters": list(self._monsters_data),
            "items": list(self._items_data)
        }
        '''
        return {
            "monsters": [m.to_dict() for m in self._monsters_data],
            "items": [i.to_dict() for i in self._items_data]
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Bag":
        '''monsters = data.get("monsters") or []
        items = data.get("items") or []
        bag = cls(monsters, items)
        return bag'''

        monsters = [Monster.from_dict(m) for m in data.get("monsters", [])]
        items = [Item.from_dict(i) for i in data.get("items", [])]
        return cls(monsters, items)
    
    def add_monster(self, monster_data):
        """添加寶可夢到背包"""
        self._monsters_data.append(monster_data)
        Logger.info(f"Added {monster_data.name} to bag")
    def del_item(self, item_name):
        for item in self._items_data:
            if item.name == item_name:
                item.count -= 1
                Logger.info(f"Used {item.name}, remaining: {item.count}")
                
                # 如果數量為 0，從背包中移除
                if item.count <= 0:
                    self._items_data.remove(item)
                    Logger.info(f"Removed {item.name} from bag (count reached 0)")
                return True
        
        Logger.warning(f"Item {item_name} not found in bag")
        return False

    
