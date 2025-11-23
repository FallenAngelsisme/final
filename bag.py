import pygame as pg
import json
from src.utils import GameSettings
from src.utils.definition import Monster, Item
from src.utils import Logger

class Bag:
    _monsters_data: list[Monster]
    _items_data: list[Item]

    def __init__(self, monsters_data: list[Monster] | None = None, items_data: list[Item] | None = None):
        self._monsters_data = monsters_data if monsters_data else []
        self._items_data = items_data if items_data else []

    def update(self, dt: float):
        pass

    def draw(self, screen: pg.Surface):
        pass

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

    
