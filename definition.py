from pygame import Rect
from .settings import GameSettings
from dataclasses import dataclass
from enum import Enum
from typing import overload, TypedDict, Protocol

MouseBtn = int
Key = int

Direction = Enum('Direction', ['UP', 'DOWN', 'LEFT', 'RIGHT', 'NONE'])

@dataclass
class Position:
    x: float
    y: float
    
    def copy(self):
        return Position(self.x, self.y)
        
    def distance_to(self, other: "Position") -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
        
@dataclass
class PositionCamera:
    x: int
    y: int
    
    def copy(self):
        return PositionCamera(self.x, self.y)
        
    def to_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)
        
    def transform_position(self, position: Position) -> tuple[int, int]:
        return (int(position.x) - self.x, int(position.y) - self.y)
        
    def transform_position_as_position(self, position: Position) -> Position:
        return Position(int(position.x) - self.x, int(position.y) - self.y)
        
    def transform_rect(self, rect: Rect) -> Rect:
        return Rect(rect.x - self.x, rect.y - self.y, rect.width, rect.height)

@dataclass
class Teleport:
    pos: Position
    destination: str
    
    @overload
    def __init__(self, x: int, y: int, destination: str) -> None: ...
    @overload
    def __init__(self, pos: Position, destination: str) -> None: ...

    def __init__(self, *args, **kwargs):
        if isinstance(args[0], Position):
            self.pos = args[0]
            self.destination = args[1]
        else:
            x, y, dest = args
            self.pos = Position(x, y)
            self.destination = dest
    
    def to_dict(self):
        return {
            "x": self.pos.x // GameSettings.TILE_SIZE,
            "y": self.pos.y // GameSettings.TILE_SIZE,
            "destination": self.destination
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["x"] * GameSettings.TILE_SIZE, data["y"] * GameSettings.TILE_SIZE, data["destination"])

from typing import Optional

class Monster:
    def __init__(
        self, name: str, hp: int, max_hp: int, level: int, sprite_path: str,
        element: str = "Normal",
        evolve_to: Optional[str] = None,
        evolve_level: Optional[int] = None
    ):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.level = level
        self.sprite_path = sprite_path
        self.element = element
        self.evolve_to = evolve_to
        self.evolve_level = evolve_level

        self.exp = 0
        self.exp_to_next_level = 100

        # 動畫控制
        self.play_level_up_anim = False
        self.play_special_level_anim = False
        self.play_evolve_anim = False

        # 可選攻擊屬性
        self.attack = getattr(self, 'attack', 10)  

    def gain_exp(self, amount: int):
        """增加經驗值並檢查升級"""
        self.exp += amount
        while self.exp >= self.exp_to_next_level:
            self.exp -= self.exp_to_next_level
            self.level_up()
            self.exp_to_next_level = int(self.exp_to_next_level * 1.5)

    def level_up(self):
        """升級：改能力值，不改圖像"""
        self.level += 1
        self.max_hp += 5 + (self.level // 5)
        self.hp = self.max_hp

        if hasattr(self, 'attack'):
            self.attack += 2 + (self.level // 10)

        # 每10等觸發特殊效果
        if self.level % 10 == 0:
            self.play_special_level_anim = True

    def can_evolve(self, evo_data) -> bool:
        """是否能進化（使用外部進化資料）"""
        if self.name not in evo_data:
            return False

        data = evo_data[self.name]
        return self.level >= data["level"]

    def evolve(self, evolution_data):
        """依照 EVOLUTION_DATA 進化怪獸，並更新名稱 / sprite_path / 屬性。"""
        if self.name not in evolution_data:
            return None

        evo = evolution_data[self.name]

        # 等級不足 → 不進化
        if self.level < evo["level"]:
            return None

        old_name = self.name
        new_name = evo["to"]

        # 更新名稱
        self.name = new_name

        # 更新圖片路徑（這一步是你缺少的！）
        self.sprite_path = evo["sprite"]

        # 更新能力
        self.max_hp += evo["stat_bonus"]["hp"]
        self.hp = self.max_hp
        self.attack += evo["stat_bonus"]["attack"]

        return old_name, new_name

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "level": self.level,
            "sprite_path": self.sprite_path,
            "element": self.element,
            "evolve_to": self.evolve_to,
            "evolve_level": self.evolve_level
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data["name"],
            hp=data["hp"],
            max_hp=data["max_hp"],
            level=data["level"],
            sprite_path=data["sprite_path"],
            element=data.get("element", "Normal"),
            evolve_to=data.get("evolve_to"),
            evolve_level=data.get("evolve_level")
        )

class Item: #(TypedDict)
    '''name: str
    count: int
    sprite_path: str'''

    def __init__(self, name: str, count: int, sprite_path: str):
        self.name = name
        self.count = count
        self.sprite_path = sprite_path

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "count": self.count,
            "sprite_path": self.sprite_path
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data["name"],
            count=data["count"],
            sprite_path=data["sprite_path"]
        )